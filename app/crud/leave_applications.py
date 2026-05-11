from sqlalchemy.orm import Session
from app.models.leave_applications import LeaveApplication
from app.schemas.leave_applications import LeaveApplicationCreate, LeaveApplicationUpdate
from typing import Optional, List

def create_leave_application(db: Session, leave: LeaveApplicationCreate) -> LeaveApplication:
    db_leave = LeaveApplication(**leave.dict())
    db.add(db_leave)
    db.commit()
    db.refresh(db_leave)
    return db_leave

def get_leave_application(db: Session, leave_id: int) -> Optional[LeaveApplication]:
    return db.query(LeaveApplication).filter(LeaveApplication.id == leave_id).first()

def get_leave_applications_by_student(db: Session, student_id: int, skip: int = 0, limit: int = 100) -> List[LeaveApplication]:
    return db.query(LeaveApplication).filter(LeaveApplication.student_id == student_id).offset(skip).limit(limit).all()

def get_leave_applications_by_status(db: Session, status: str, skip: int = 0, limit: int = 100) -> List[LeaveApplication]:
    return db.query(LeaveApplication).filter(LeaveApplication.status == status).offset(skip).limit(limit).all()

def update_leave_application(db: Session, leave_id: int, leave_update: LeaveApplicationUpdate) -> Optional[LeaveApplication]:
    db_leave = db.query(LeaveApplication).filter(LeaveApplication.id == leave_id).first()
    if db_leave:
        update_data = leave_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_leave, key, value)
        db.commit()
        db.refresh(db_leave)
    return db_leave