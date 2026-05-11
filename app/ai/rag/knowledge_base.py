import os
import json
from typing import List, Dict, Any, Optional
from app.ai.rag.vector_store import VectorStore
from app.core.logger import logger

class KnowledgeBase:
    def __init__(self):
        self.vector_store = VectorStore()
        self.knowledge_dir = "knowledge_base"
        os.makedirs(self.knowledge_dir, exist_ok=True)

    def add_knowledge(self, title: str, content: str, category: str = "general") -> int:
        metadata = {
            "title": title,
            "category": category,
            "created_at": os.path.getctime(__file__)
        }
        
        doc_id = self.vector_store.add_document(content, metadata)
        
        json_path = os.path.join(self.knowledge_dir, f"{doc_id}.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump({
                "id": doc_id,
                "title": title,
                "content": content,
                "category": category
            }, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Added knowledge: {title} (id: {doc_id})")
        return doc_id

    def search_knowledge(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        query_embedding = self._generate_query_embedding(query)
        results = self.vector_store.search(query_embedding, top_k)
        
        logger.info(f"Search completed for query: '{query}', found {len(results)} results")
        return results

    def _generate_query_embedding(self, query: str) -> List[float]:
        import random
        return [random.random() for _ in range(1536)]

    def get_knowledge_by_id(self, doc_id: int) -> Optional[Dict[str, Any]]:
        return self.vector_store.get_document(doc_id)

    def delete_knowledge(self, doc_id: int) -> bool:
        success = self.vector_store.delete_document(doc_id)
        
        json_path = os.path.join(self.knowledge_dir, f"{doc_id}.json")
        if os.path.exists(json_path):
            os.remove(json_path)
        
        if success:
            logger.info(f"Deleted knowledge: {doc_id}")
        return success

    def list_knowledge(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        knowledge_list = []
        
        for filename in os.listdir(self.knowledge_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(self.knowledge_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if category is None or data.get("category") == category:
                            knowledge_list.append(data)
                except Exception as e:
                    logger.error(f"Failed to read knowledge file {filename}: {e}")
        
        return sorted(knowledge_list, key=lambda x: x.get("created_at", 0), reverse=True)

    def load_from_directory(self, directory: str):
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                filepath = os.path.join(directory, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    title = os.path.splitext(filename)[0]
                    self.add_knowledge(title, content)
                    logger.info(f"Loaded knowledge from file: {filename}")
                except Exception as e:
                    logger.error(f"Failed to load knowledge from {filename}: {e}")

    def retrieve_for_rag(self, query: str, context_size: int = 3) -> str:
        results = self.search_knowledge(query, top_k=context_size)
        
        if not results:
            return ""
        
        context_parts = []
        for i, result in enumerate(results, 1):
            content = result.get("content", "")[:500]
            title = result.get("metadata", {}).get("title", "Unknown")
            context_parts.append(f"【知识片段{i}】标题：{title}\n内容：{content}")
        
        return "\n\n".join(context_parts)