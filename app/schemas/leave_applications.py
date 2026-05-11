from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class LeaveApplicationBase(BaseModel):
    student_id: int
    student_name: str
    leave_type: str
    start_date: date
    end_date: date
    reason: Optional[str] = None

class LeaveApplicationCreate(LeaveApplicationBase):
    pass

class LeaveApplicationUpdate(BaseModel):
    status: Optional[str] = None
    approver_id: Optional[int] = None
    approver_name: Optional[str] = None
    approve_comment: Optional[str] = None

class LeaveApplicationResponse(LeaveApplicationBase):
    id: int
    status: str
    approver_id: Optional[int] = None
    approver_name: Optional[str] = None
    approve_comment: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True