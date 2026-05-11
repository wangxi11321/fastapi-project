from typing import Dict, Any
from sqlalchemy.orm import Session
from app.ai.agents.customer_agent import CustomerAgent
from app.crud.intent_customers import create_intent_customer
from app.schemas.intent_customers import IntentCustomerCreate
from app.core.logger import logger

class CustomerWorkflow:
    def __init__(self, db: Session):
        self.db = db
        self.customer_agent = CustomerAgent()

    def execute_judgment(self, customer_info: str) -> Dict[str, Any]:
        logger.info("Starting customer judgment workflow")
        
        try:
            judge_result = self._judge_customer(customer_info)
            
            if judge_result["is_target"]:
                customer_data = self._create_customer(judge_result)
                judge_result["customer_created"] = True
                judge_result["customer_id"] = customer_data.id
                self._notify_assignment(customer_data)
            else:
                judge_result["customer_created"] = False
                judge_result["customer_id"] = None
            
            return judge_result
            
        except Exception as e:
            logger.error(f"Customer judgment workflow failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "is_target": False,
                "reason": "流程执行失败",
                "customer_created": False
            }

    def _judge_customer(self, customer_info: str) -> Dict[str, Any]:
        logger.info("Executing customer judgment")
        return self.customer_agent.analyze_customer(customer_info)

    def _create_customer(self, judge_result: Dict[str, Any]) -> Any:
        logger.info("Creating customer record")
        extracted = judge_result["extracted_info"]
        
        customer_create = IntentCustomerCreate(
            name=extracted.get("name") or "未知",
            phone=extracted.get("phone") or "未知",
            email=extracted.get("email"),
            education=extracted.get("education"),
            major=extracted.get("major"),
            budget=extracted.get("budget"),
            country=extracted.get("country"),
            english_level=extracted.get("english_level"),
            target_school=extracted.get("target_school"),
            target_major=extracted.get("target_major"),
            tags=judge_result.get("tags"),
            is_target=judge_result.get("is_target"),
            judge_reason=judge_result.get("reason")
        )
        
        return create_intent_customer(self.db, customer_create)

    def _notify_assignment(self, customer_data: Any):
        logger.info(f"Notifying assignment for customer {customer_data.id}")