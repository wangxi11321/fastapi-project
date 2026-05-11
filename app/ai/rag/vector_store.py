import os
import json
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.core.logger import logger

try:
    from pgvector.sqlalchemy import Vector
    import psycopg2
    HAS_PGVECTOR = True
except ImportError:
    HAS_PGVECTOR = False
    logger.warning("pgvector not installed, using mock implementation")

class VectorStore:
    def __init__(self):
        self.embedding_dim = 1536
        self.collection_name = "knowledge_base"
        self._initialize_store()

    def _initialize_store(self):
        if HAS_PGVECTOR:
            try:
                self._setup_pgvector()
            except Exception as e:
                logger.error(f"Failed to setup pgvector: {e}")
                self._use_mock_store()
        else:
            self._use_mock_store()

    def _setup_pgvector(self):
        self.use_pgvector = True
        logger.info("Using pgvector for vector storage")

    def _use_mock_store(self):
        self.use_pgvector = False
        self._mock_store = []
        logger.info("Using mock vector store")

    def add_document(self, content: str, metadata: Dict[str, Any], embedding: Optional[List[float]] = None):
        if not embedding:
            embedding = self._generate_mock_embedding()
        
        doc = {
            "content": content,
            "metadata": metadata,
            "embedding": embedding,
            "id": len(self._mock_store) + 1
        }
        
        if self.use_pgvector:
            self._add_to_pgvector(doc)
        else:
            self._mock_store.append(doc)
        
        logger.info(f"Added document to vector store: {metadata.get('title', 'unknown')}")
        return doc["id"]

    def _add_to_pgvector(self, doc: Dict[str, Any]):
        pass

    def _generate_mock_embedding(self) -> List[float]:
        import random
        return [random.random() for _ in range(self.embedding_dim)]

    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        if self.use_pgvector:
            return self._search_pgvector(query_embedding, top_k)
        else:
            return self._search_mock(query_embedding, top_k)

    def _search_pgvector(self, query_embedding: List[float], top_k: int) -> List[Dict[str, Any]]:
        return []

    def _search_mock(self, query_embedding: List[float], top_k: int) -> List[Dict[str, Any]]:
        results = []
        for doc in self._mock_store:
            similarity = self._cosine_similarity(query_embedding, doc["embedding"])
            results.append({
                "content": doc["content"],
                "metadata": doc["metadata"],
                "similarity": similarity
            })
        
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]

    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        dot_product = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5
        return dot_product / (norm_a * norm_b) if norm_a and norm_b else 0.0

    def delete_document(self, doc_id: int) -> bool:
        if self.use_pgvector:
            return self._delete_from_pgvector(doc_id)
        else:
            original_length = len(self._mock_store)
            self._mock_store = [d for d in self._mock_store if d["id"] != doc_id]
            return len(self._mock_store) < original_length

    def _delete_from_pgvector(self, doc_id: int) -> bool:
        return False

    def get_document(self, doc_id: int) -> Optional[Dict[str, Any]]:
        if self.use_pgvector:
            return self._get_from_pgvector(doc_id)
        else:
            return next((d for d in self._mock_store if d["id"] == doc_id), None)

    def _get_from_pgvector(self, doc_id: int) -> Optional[Dict[str, Any]]:
        return None

    def clear(self):
        if self.use_pgvector:
            self._clear_pgvector()
        else:
            self._mock_store = []
        logger.info("Vector store cleared")

    def _clear_pgvector(self):
        pass