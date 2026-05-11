from sqlalchemy import Column, Integer, String, Text, Date, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class DailyReport(Base):
    __tablename__ = "daily_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, nullable=False)
    employee_name = Column(String(100), nullable=False)
    date = Column(Date, nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text)
    tasks_done = Column(Text)
    tasks_tomorrow = Column(Text)
    issues = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())