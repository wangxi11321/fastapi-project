from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from app.models.intent_customers import IntentCustomer
from app.schemas.intent_customers import IntentCustomerCreate, IntentCustomerUpdate
from app.crud.intent_customers import (
    create_intent_customer,
    get_intent_customer,
    get_intent_customer_by_phone,
    get_intent_customers,
    update_intent_customer,
    delete_intent_customer
)
from app.ai.agents.customer_agent import CustomerAgent
from app.ai.workflows.customer_workflow import CustomerWorkflow
from app.core.logger import logger

class CustomerService:
    def __init__(self, db: Session):
        self.db = db
        self.customer_agent = CustomerAgent()
        self.workflow = CustomerWorkflow(db)

    def create_customer(self, customer_data: IntentCustomerCreate) -> IntentCustomer:
        logger.info(f"Creating customer: {customer_data.name}")
        db_customer = create_intent_customer(self.db, customer_data)
        logger.info(f"Customer created with id: {db_customer.id}")
        return db_customer

    def get_customer(self, customer_id: int) -> Optional[IntentCustomer]:
        return get_intent_customer(self.db, customer_id)

    def get_customer_by_phone(self, phone: str) -> Optional[IntentCustomer]:
        return get_intent_customer_by_phone(self.db, phone)

    def get_customers(self, skip: int = 0, limit: int = 100) -> List[IntentCustomer]:
        return get_intent_customers(self.db, skip, limit)

    def update_customer(self, customer_id: int, update_data: IntentCustomerUpdate) -> Optional[IntentCustomer]:
        logger.info(f"Updating customer: {customer_id}")
        db_customer = update_intent_customer(self.db, customer_id, update_data)
        if db_customer:
            logger.info(f"Customer updated: {customer_id}")
        return db_customer

    def delete_customer(self, customer_id: int) -> bool:
        logger.info(f"Deleting customer: {customer_id}")
        success = delete_intent_customer(self.db, customer_id)
        if success:
            logger.info(f"Customer deleted: {customer_id}")
        return success

    def judge_and_create_customer(self, customer_info: str) -> Dict[str, Any]:
        logger.info("Starting customer judgment workflow")
        result = self.workflow.execute_judgment(customer_info)
        return result

    def assign_customer(self, customer_id: int, assignee: str) -> Optional[IntentCustomer]:
        logger.info(f"Assigning customer {customer_id} to {assignee}")
        update_data = IntentCustomerUpdate(assignee=assignee, status="assigned")
        return update_intent_customer(self.db, customer_id, update_data)