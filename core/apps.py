from django.apps import AppConfig

class CoreConfig(AppConfig):
    name = 'core'
    
    def ready(self):
        from core.services.load_faiss import load_embeddings
        load_embeddings()
