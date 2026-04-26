import faiss
import numpy as np
from typing import List, Tuple

class VectorStore:
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.documents = []

    def add_documents(self, embeddings: List[List[float]], docs: List[str]):
        embeddings_np = np.array(embeddings, dtype=np.float32)
        self.index.add(embeddings_np)
        self.documents.extend(docs)

    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Tuple[str, float]]:
        query_np = np.array([query_embedding], dtype=np.float32)
        distances, indices = self.index.search(query_np, top_k)
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.documents):
                results.append((self.documents[idx], float(dist)))
        return results