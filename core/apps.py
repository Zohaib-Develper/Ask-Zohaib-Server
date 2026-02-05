import sys
from django.apps import AppConfig

class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        # Skip loading embeddings during collectstatic or migrate
        if any(cmd in sys.argv for cmd in ['collectstatic', 'migrate', 'makemigrations']):
            return

        try:
            from core.services.load_faiss import load_embeddings
            load_embeddings()
        except Exception as e:
            print(f"[FAISS] Skipping embedding load: {e}")
