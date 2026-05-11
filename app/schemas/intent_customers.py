from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional, List

class IntentCustomerBase(BaseModel):
    name: str
    phone: str
    email: Optional[EmailStr] = None
    source: Optional[str] = None
    country: Optional[str] = None
    education: Optional[str] = None
    major: Optional[str] = None
    budget: Optional[float] = None
    target_school: Optional[str] = None
    target_major: Optional[str] = None
    english_level: Optional[str] = None
    tags: Optional[str] = None
    assignee: Optional[str] = None
    status: Optional[str] = "pending"

class IntentCustomerCreate(IntentCustomerBase):
    pass

class IntentCustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    source: Optional[str] = None
    country: Optional[str] = None
    education: Optional[str] = None
    major: Optional[str] = None
    budget: Optional[float] = None
    target_school: Optional[str] = None
    target_major: Optional[str] = None
    english_level: Optional[str] = None
    tags: Optional[str] = None
    is_target: Optional[bool] = None
    judge_reason: Optional[str] = None
    assignee: Optional[str] = None
    status: Optional[str] = None

class IntentCustomerResponse(IntentCustomerBase):
    id: int
    is_target: bool
    judge_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CustomerJudgeRequest(BaseModel):
    customer_info: str
    file_path: Optional[str] = None