from django.db import models

# Create your models here.
class Document(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
class Chunk(models.Model):
    document =models.ForeignKey(Document, on_delete=models.CASCADE, related_name='chunks')
    chunk = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.document.title} - Chunk {self.id}"