import pdfplumber
from docx import Document

class FileContentExtractor:
    @staticmethod
    def extract(file):
        name = file.name.lower()
        
        if(name.endswith('.pdf')):
            return FileContentExtractor.get_content_from_pdf(file)
        elif(name.endswith(('.docx', 'doc'))):
            return FileContentExtractor.get_content_from_docx(file)
        elif name.endswith('.txt'):
            return FileContentExtractor.get_content_from_txt(file)
        
        raise ValueError("Unsupported file")
    @staticmethod
    def get_content_from_pdf(file):
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    @staticmethod
    def get_content_from_docx(file):
        doc = Document(file)
        return '\n'.join(p.text for p in doc.paragraphs)
    @staticmethod
    def get_content_from_txt(file):
        try:
            return file.read().decode('utf-8')
        except UnicodeDecodeError:
            file.seek(0)
            return file.read().decode('latin-1')
        
    @staticmethod
    def split_content_to_chunks(content, words_per_chunk, overlap):
        words = content.split()
        
        chunked_text = [ " ".join(words[i:i+words_per_chunk]) 
                        for i in range(0,len(words),words_per_chunk-overlap)
                        if i<len(words)]
        
        return chunked_text
        