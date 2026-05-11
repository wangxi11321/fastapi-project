from celery import shared_task
from app.core.logger import logger
from app.ai.agents.customer_agent import CustomerAgent

@shared_task
def judge_customer_task(customer_info: str):
    try:
        agent = CustomerAgent()
        result = agent.analyze_customer(customer_info)
        logger.info(f"Customer judgment completed: is_target={result['is_target']}")
        return {"status": "success", "result": result}
    except Exception as e:
        logger.error(f"Failed to judge customer: {e}")
        return {"status": "failed", "error": str(e)}

@shared_task
def process_knowledge_document(doc_id: int, content: str, metadata: dict):
    try:
        from app.ai.rag.knowledge_base import KnowledgeBase
        
        kb = KnowledgeBase()
        kb.add_knowledge(
            title=metadata.get("title", f"Document {doc_id}"),
            content=content,
            category=metadata.get("category", "general")
        )
        logger.info(f"Knowledge document processed: {doc_id}")
        return {"status": "success", "doc_id": doc_id}
    except Exception as e:
        logger.error(f"Failed to process knowledge document: {e}")
        return {"status": "failed", "error": str(e)}

@shared_task
def generate_embeddings(text: str):
    try:
        logger.info(f"Generating embeddings for text of length {len(text)}")
        import random
        embedding = [random.random() for _ in range(1536)]
        return {"status": "success", "embedding_length": len(embedding)}
    except Exception as e:
        logger.error(f"Failed to generate embeddings: {e}")
        return {"status": "failed", "error": str(e)}