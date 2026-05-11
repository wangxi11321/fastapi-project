from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.leave_service import LeaveService
from app.schemas.leave_applications import LeaveApplicationCreate, LeaveApplicationUpdate, LeaveApplicationResponse
from typing import List, Dict, Any

router = APIRouter()

def get_leave_service(db: Session = Depends(get_db)) -> LeaveService:
    return LeaveService(db)

@router.post("/", response_model=LeaveApplicationResponse)
def create_leave_application(
    leave: LeaveApplicationCreate,
    service: LeaveService = Depends(get_leave_service)
):
    db_leave = service.create_leave_application(leave)
    return db_leave

@router.get("/", response_model=List[LeaveApplicationResponse])
def read_leaves(
    status: str = None,
    student_id: int = None,
    service: LeaveService = Depends(get_leave_service)
):
    if student_id:
        leaves = service.get_leave_applications_by_student(student_id)
    elif status:
        leaves = service.get_leave_applications_by_status(status)
    else:
        leaves = service.get_leave_applications_by_status("pending")
    return leaves

@router.get("/{leave_id}", response_model=LeaveApplicationResponse)
def read_leave(
    leave_id: int,
    service: LeaveService = Depends(get_leave_service)
):
    db_leave = service.get_leave_application(leave_id)
    if db_leave is None:
        raise HTTPException(status_code=404, detail="请假申请不存在")
    return db_leave

@router.put("/{leave_id}", response_model=LeaveApplicationResponse)
def update_leave(
    leave_id: int,
    leave: LeaveApplicationUpdate,
    service: LeaveService = Depends(get_leave_service)
):
    db_leave = service.update_leave_application(leave_id, leave)
    if db_leave is None:
        raise HTTPException(status_code=404, detail="请假申请不存在")
    return db_leave

@router.delete("/{leave_id}")
def delete_leave(
    leave_id: int,
    service: LeaveService = Depends(get_leave_service)
):
    success = service.delete_leave_application(leave_id)
    if not success:
        raise HTTPException(status_code=404, detail="请假申请不存在")
    return {"message": "请假申请删除成功"}

@router.post("/apply")
def apply_leave(
    data: Dict[str, Any],
    service: LeaveService = Depends(get_leave_service)
):
    result = service.apply_leave(data)
    return result

@router.post("/{leave_id}/approve")
def approve_leave(
    leave_id: int,
    approver_id: int,
    approver_name: str,
    comment: str = "",
    service: LeaveService = Depends(get_leave_service)
):
    db_leave = service.approve_leave(leave_id, approver_id, approver_name, comment)
    if db_leave is None:
        raise HTTPException(status_code=404, detail="请假申请不存在")
    return db_leave

@router.post("/{leave_id}/reject")
def reject_leave(
    leave_id: int,
    approver_id: int,
    approver_name: str,
    comment: str = "",
    service: LeaveService = Depends(get_leave_service)
):
    db_leave = service.reject_leave(leave_id, approver_id, approver_name, comment)
    if db_leave is None:
        raise HTTPException(status_code=404, detail="请假申请不存在")
    return db_leave