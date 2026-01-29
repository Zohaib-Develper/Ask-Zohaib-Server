from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingService:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
    def get_embedding(self, text: str) -> np.ndarray:
        vector = self.model.encode(text)
        return vector.astype("float32")