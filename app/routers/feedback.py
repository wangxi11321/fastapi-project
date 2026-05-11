from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.feedback_tickets import (
    create_feedback_ticket,
    get_feedback_ticket,
    get_feedback_tickets,
    get_feedback_tickets_by_status,
    update_feedback_ticket,
    delete_feedback_ticket
)
from app.schemas.feedback_tickets import FeedbackTicketCreate, FeedbackTicketUpdate, FeedbackTicketResponse
from typing import List

router = APIRouter()

@router.post("/", response_model=FeedbackTicketResponse)
def create_feedback(feedback: FeedbackTicketCreate, db: Session = Depends(get_db)):
    db_feedback = create_feedback_ticket(db=db, feedback=feedback)
    return db_feedback

@router.get("/", response_model=List[FeedbackTicketResponse])
def read_feedbacks(
    status: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    if status:
        feedbacks = get_feedback_tickets_by_status(db, status=status)
    else:
        feedbacks = get_feedback_tickets(db, skip=skip, limit=limit)
    return feedbacks

@router.get("/{feedback_id}", response_model=FeedbackTicketResponse)
def read_feedback(feedback_id: int, db: Session = Depends(get_db)):
    db_feedback = get_feedback_ticket(db, feedback_id=feedback_id)
    if db_feedback is None:
        raise HTTPException(status_code=404, detail="反馈不存在")
    return db_feedback

@router.put("/{feedback_id}", response_model=FeedbackTicketResponse)
def update_feedback(feedback_id: int, feedback: FeedbackTicketUpdate, db: Session = Depends(get_db)):
    db_feedback = update_feedback_ticket(db, feedback_id=feedback_id, feedback_update=feedback)
    if db_feedback is None:
        raise HTTPException(status_code=404, detail="反馈不存在")
    return db_feedback

@router.delete("/{feedback_id}")
def delete_feedback(feedback_id: int, db: Session = Depends(get_db)):
    success = delete_feedback_ticket(db, feedback_id=feedback_id)
    if not success:
        raise HTTPException(status_code=404, detail="反馈不存在")
    return {"message": "反馈删除成功"}