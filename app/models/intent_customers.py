from sqlalchemy import Column, Integer, String, Text, Date, Float, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class IntentCustomer(Base):
    __tablename__ = "intent_customers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False, unique=True)
    email = Column(String(100))
    source = Column(String(50))
    country = Column(String(50))
    education = Column(String(50))
    major = Column(String(100))
    budget = Column(Float)
    target_school = Column(String(200))
    target_major = Column(String(100))
    english_level = Column(String(50))
    tags = Column(Text)
    is_target = Column(Boolean, default=False)
    judge_reason = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    assignee = Column(String(100))
    status = Column(String(20), default="pending")