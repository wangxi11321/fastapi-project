from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.leave_applications import create_leave_application, get_leave_application, get_leave_applications_by_student, get_leave_applications_by_status, update_leave_application
from app.schemas.leave_applications import LeaveApplicationCreate, LeaveApplicationUpdate, LeaveApplicationResponse
from typing import List

router = APIRouter()

@router.post("/", response_model=LeaveApplicationResponse)
def create_leave(leave: LeaveApplicationCreate, db: Session = Depends(get_db)):
    db_leave = create_leave_application(db=db, leave=leave)
    return db_leave

@router.get("/{leave_id}", response_model=LeaveApplicationResponse)
def read_leave(leave_id: int, db: Session = Depends(get_db)):
    db_leave = get_leave_application(db, leave_id=leave_id)
    if db_leave is None:
        raise HTTPException(status_code=404, detail="请假申请不存在")
    return db_leave

@router.get("/student/{student_id}", response_model=List[LeaveApplicationResponse])
def read_leaves_by_student(student_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    leaves = get_leave_applications_by_student(db, student_id=student_id, skip=skip, limit=limit)
    return leaves

@router.get("/status/{status}", response_model=List[LeaveApplicationResponse])
def read_leaves_by_status(status: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    leaves = get_leave_applications_by_status(db, status=status, skip=skip, limit=limit)
    return leaves

@router.put("/{leave_id}", response_model=LeaveApplicationResponse)
def update_leave(leave_id: int, leave: LeaveApplicationUpdate, db: Session = Depends(get_db)):
    db_leave = update_leave_application(db, leave_id=leave_id, leave_update=leave)
    if db_leave is None:
        raise HTTPException(status_code=404, detail="请假申请不存在")
    return db_leave