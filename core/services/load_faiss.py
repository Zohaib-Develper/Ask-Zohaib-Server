from core.services.faiss_service import FaissService
from core.services.embedding_service import EmbeddingService

faiss_service = FaissService()
embedding_service = EmbeddingService()

def load_embeddings():
    from core.models import Chunk
    chunks =Chunk.objects.all()
    
    for chunk in chunks:
        embedding = embedding_service.get_embedding(chunk.chunk)
        faiss_service.add_chunk(chunk.id, embedding_vector=embedding)
        
    print("[FAISS] loaded ", len(chunks), " in memory")