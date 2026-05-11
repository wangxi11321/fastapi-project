from sqlalchemy.orm import Session
from app.models.intent_customers import IntentCustomer
from app.schemas.intent_customers import IntentCustomerCreate, IntentCustomerUpdate
from typing import Optional, List

def create_intent_customer(db: Session, customer: IntentCustomerCreate) -> IntentCustomer:
    db_customer = IntentCustomer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def get_intent_customer(db: Session, customer_id: int) -> Optional[IntentCustomer]:
    return db.query(IntentCustomer).filter(IntentCustomer.id == customer_id).first()

def get_intent_customer_by_phone(db: Session, phone: str) -> Optional[IntentCustomer]:
    return db.query(IntentCustomer).filter(IntentCustomer.phone == phone).first()

def get_intent_customers(db: Session, skip: int = 0, limit: int = 100) -> List[IntentCustomer]:
    return db.query(IntentCustomer).offset(skip).limit(limit).all()

def update_intent_customer(db: Session, customer_id: int, customer_update: IntentCustomerUpdate) -> Optional[IntentCustomer]:
    db_customer = db.query(IntentCustomer).filter(IntentCustomer.id == customer_id).first()
    if db_customer:
        update_data = customer_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_customer, key, value)
        db.commit()
        db.refresh(db_customer)
    return db_customer

def delete_intent_customer(db: Session, customer_id: int) -> bool:
    db_customer = db.query(IntentCustomer).filter(IntentCustomer.id == customer_id).first()
    if db_customer:
        db.delete(db_customer)
        db.commit()
        return True
    return False