from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.feedback_tickets import create_feedback_ticket, get_feedback_ticket, get_feedback_tickets_by_student, get_feedback_tickets_by_status, update_feedback_ticket
from app.schemas.feedback_tickets import FeedbackTicketCreate, FeedbackTicketUpdate, FeedbackTicketResponse
from typing import List

router = APIRouter()

@router.post("/", response_model=FeedbackTicketResponse)
def create_feedback(feedback: FeedbackTicketCreate, db: Session = Depends(get_db)):
    db_feedback = create_feedback_ticket(db=db, feedback=feedback)
    return db_feedback

@router.get("/{ticket_id}", response_model=FeedbackTicketResponse)
def read_feedback(ticket_id: int, db: Session = Depends(get_db)):
    db_feedback = get_feedback_ticket(db, ticket_id=ticket_id)
    if db_feedback is None:
        raise HTTPException(status_code=404, detail="反馈工单不存在")
    return db_feedback

@router.get("/student/{student_id}", response_model=List[FeedbackTicketResponse])
def read_feedback_by_student(student_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    feedbacks = get_feedback_tickets_by_student(db, student_id=student_id, skip=skip, limit=limit)
    return feedbacks

@router.get("/status/{status}", response_model=List[FeedbackTicketResponse])
def read_feedback_by_status(status: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    feedbacks = get_feedback_tickets_by_status(db, status=status, skip=skip, limit=limit)
    return feedbacks

@router.put("/{ticket_id}", response_model=FeedbackTicketResponse)
def update_feedback(ticket_id: int, feedback: FeedbackTicketUpdate, db: Session = Depends(get_db)):
    db_feedback = update_feedback_ticket(db, ticket_id=ticket_id, feedback_update=feedback)
    if db_feedback is None:
        raise HTTPException(status_code=404, detail="反馈工单不存在")
    return db_feedback