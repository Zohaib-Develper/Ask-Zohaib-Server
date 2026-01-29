from django.contrib import admin

# Register your models here.
from .models import Document
from django import forms
from core.services.file_content_extractor import FileContentExtractor
from .models import Chunk
from django.db import transaction

class DocumentAdminForm(forms.ModelForm):
    upload_text_file = forms.FileField(required=True, help_text="Upload a PDF or .DOCX file to populate content")

    class Meta:
        model = Document
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["content"].required = False
        
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    form = DocumentAdminForm
    list_display= ('title',)

    def save_model(self, request, obj, form, change):
        uploaded_file = form.cleaned_data.get('upload_text_file')
        
        if uploaded_file:
            content = FileContentExtractor.extract(uploaded_file)
            obj.content = content
        
            with transaction.atomic():
                super().save_model(request, obj, form, change)
                if change:
                    obj.chunks.all().delete()
                chunks_text = FileContentExtractor.split_content_to_chunks(content, 350, 50)
                chunk_objects = [
                    Chunk(document=obj, chunk=text) 
                    for text in chunks_text
                ]
                Chunk.objects.bulk_create(chunk_objects)
                from core.services.load_faiss import load_embeddings
                load_embeddings()

        else:
            super().save_model(request, obj, form, change)
            
@admin.register(Chunk)
class ChunkAdmin(admin.ModelAdmin):
    list_display=('chunk',)
