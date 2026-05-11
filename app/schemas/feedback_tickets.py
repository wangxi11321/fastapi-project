from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FeedbackTicketBase(BaseModel):
    student_id: int
    student_name: str
    type: str
    content: str

class FeedbackTicketCreate(FeedbackTicketBase):
    pass

class FeedbackTicketUpdate(BaseModel):
    status: Optional[str] = None
    handler_id: Optional[int] = None
    handler_name: Optional[str] = None
    reply: Optional[str] = None

class FeedbackTicketResponse(FeedbackTicketBase):
    id: int
    status: str
    handler_id: Optional[int] = None
    handler_name: Optional[str] = None
    reply: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True