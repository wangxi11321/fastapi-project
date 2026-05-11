from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class ActivityBase(BaseModel):
    name: str
    type: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    capacity: Optional[int] = None
    is_active: Optional[bool] = True

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    capacity: Optional[int] = None
    is_active: Optional[bool] = None

class ActivityResponse(ActivityBase):
    id: int
    registered_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ActivityRegisterRequest(BaseModel):
    activity_id: int
    student_id: int
    student_name: str