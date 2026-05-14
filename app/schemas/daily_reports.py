from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class DailyReportBase(BaseModel):
    employee_id: int
    employee_name: str
    date: date
    content: str
    summary: Optional[str] = None
    tasks_done: Optional[str] = None
    tasks_tomorrow: Optional[str] = None
    issues: Optional[str] = None

class DailyReportCreate(DailyReportBase):
    pass

class DailyReportResponse(DailyReportBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DailyReportUpdate(BaseModel):
    employee_id: Optional[int] = None
    employee_name: Optional[str] = None
    date: Optional[date] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    tasks_done: Optional[str] = None
    tasks_tomorrow: Optional[str] = None
    issues: Optional[str] = None

class DailyReportSummary(BaseModel):
    date: date
    total_reports: int
    summary_content: str