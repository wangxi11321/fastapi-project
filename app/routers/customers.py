from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.customer_service import CustomerService
from app.schemas.intent_customers import IntentCustomerCreate, IntentCustomerUpdate, IntentCustomerResponse
from typing import List

router = APIRouter()

def get_customer_service(db: Session = Depends(get_db)) -> CustomerService:
    return CustomerService(db)

@router.post("/", response_model=IntentCustomerResponse)
def create_customer(
    customer: IntentCustomerCreate,
    service: CustomerService = Depends(get_customer_service)
):
    db_customer = service.create_customer(customer)
    return db_customer

@router.get("/", response_model=List[IntentCustomerResponse])
def read_customers(
    skip: int = 0,
    limit: int = 100,
    service: CustomerService = Depends(get_customer_service)
):
    customers = service.get_customers(skip=skip, limit=limit)
    return customers

@router.get("/{customer_id}", response_model=IntentCustomerResponse)
def read_customer(
    customer_id: int,
    service: CustomerService = Depends(get_customer_service)
):
    db_customer = service.get_customer(customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="客户不存在")
    return db_customer

@router.put("/{customer_id}", response_model=IntentCustomerResponse)
def update_customer(
    customer_id: int,
    customer: IntentCustomerUpdate,
    service: CustomerService = Depends(get_customer_service)
):
    db_customer = service.update_customer(customer_id, customer)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="客户不存在")
    return db_customer

@router.delete("/{customer_id}")
def delete_customer(
    customer_id: int,
    service: CustomerService = Depends(get_customer_service)
):
    success = service.delete_customer(customer_id)
    if not success:
        raise HTTPException(status_code=404, detail="客户不存在")
    return {"message": "客户删除成功"}

@router.post("/judge")
def judge_customer(
    customer_info: str,
    service: CustomerService = Depends(get_customer_service)
):
    result = service.judge_and_create_customer(customer_info)
    return result

@router.post("/{customer_id}/assign")
def assign_customer(
    customer_id: int,
    assignee: str,
    service: CustomerService = Depends(get_customer_service)
):
    db_customer = service.assign_customer(customer_id, assignee)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="客户不存在")
    return db_customer