import faiss
import numpy as np
from core.models import Chunk

class FaissService:
    def __init__(self, dim = 384):
        self.index = faiss.IndexFlatIP(dim)
        self.id_map = {}
        self.current_index = 0
        
    def add_chunk(self, chunk_id, embedding_vector: np.ndarray):
        self.index.add(np.array([embedding_vector]))
        self.id_map[self.current_index] = chunk_id
        self.current_index += 1
        
    def search(self, query_vector: np.ndarray, top_k = 5):
        D, I = self.index.search(np.array([query_vector]), top_k)
        results = []
        for i in I[0]:
            chunk_id = self.id_map.get(i)
            if chunk_id:
                chunk = Chunk.objects.get(id=chunk_id)
                results.append(chunk.chunk)
        return results