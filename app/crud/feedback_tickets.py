from sqlalchemy.orm import Session
from app.models.feedback_tickets import FeedbackTicket
from app.schemas.feedback_tickets import FeedbackTicketCreate, FeedbackTicketUpdate
from typing import Optional, List

def create_feedback_ticket(db: Session, feedback: FeedbackTicketCreate) -> FeedbackTicket:
    db_feedback = FeedbackTicket(**feedback.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def get_feedback_ticket(db: Session, ticket_id: int) -> Optional[FeedbackTicket]:
    return db.query(FeedbackTicket).filter(FeedbackTicket.id == ticket_id).first()

def get_feedback_tickets_by_student(db: Session, student_id: int, skip: int = 0, limit: int = 100) -> List[FeedbackTicket]:
    return db.query(FeedbackTicket).filter(FeedbackTicket.student_id == student_id).offset(skip).limit(limit).all()

def get_feedback_tickets_by_status(db: Session, status: str, skip: int = 0, limit: int = 100) -> List[FeedbackTicket]:
    return db.query(FeedbackTicket).filter(FeedbackTicket.status == status).offset(skip).limit(limit).all()

def update_feedback_ticket(db: Session, ticket_id: int, feedback_update: FeedbackTicketUpdate) -> Optional[FeedbackTicket]:
    db_feedback = db.query(FeedbackTicket).filter(FeedbackTicket.id == ticket_id).first()
    if db_feedback:
        update_data = feedback_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_feedback, key, value)
        db.commit()
        db.refresh(db_feedback)
    return db_feedback