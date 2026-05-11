from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.intent_customers import create_intent_customer, get_intent_customer, get_intent_customers, update_intent_customer, delete_intent_customer
from app.schemas.intent_customers import IntentCustomerCreate, IntentCustomerUpdate, IntentCustomerResponse
from typing import List

router = APIRouter()

@router.post("/", response_model=IntentCustomerResponse)
def create_customer(customer: IntentCustomerCreate, db: Session = Depends(get_db)):
    db_customer = create_intent_customer(db=db, customer=customer)
    return db_customer

@router.get("/", response_model=List[IntentCustomerResponse])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = get_intent_customers(db, skip=skip, limit=limit)
    return customers

@router.get("/{customer_id}", response_model=IntentCustomerResponse)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = get_intent_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="客户不存在")
    return db_customer

@router.put("/{customer_id}", response_model=IntentCustomerResponse)
def update_customer(customer_id: int, customer: IntentCustomerUpdate, db: Session = Depends(get_db)):
    db_customer = update_intent_customer(db, customer_id=customer_id, customer_update=customer)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="客户不存在")
    return db_customer

@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    success = delete_intent_customer(db, customer_id=customer_id)
    if not success:
        raise HTTPException(status_code=404, detail="客户不存在")
    return {"message": "客户删除成功"}