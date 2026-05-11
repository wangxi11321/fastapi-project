from sqlalchemy.orm import Session
from app.models.activities import Activity
from app.schemas.activities import ActivityCreate, ActivityUpdate
from typing import Optional, List

def create_activity(db: Session, activity: ActivityCreate) -> Activity:
    db_activity = Activity(**activity.dict())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

def get_activity(db: Session, activity_id: int) -> Optional[Activity]:
    return db.query(Activity).filter(Activity.id == activity_id).first()

def get_activities(db: Session, skip: int = 0, limit: int = 100) -> List[Activity]:
    return db.query(Activity).filter(Activity.is_active == True).offset(skip).limit(limit).all()

def update_activity(db: Session, activity_id: int, activity_update: ActivityUpdate) -> Optional[Activity]:
    db_activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if db_activity:
        update_data = activity_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_activity, key, value)
        db.commit()
        db.refresh(db_activity)
    return db_activity

def register_activity(db: Session, activity_id: int) -> bool:
    db_activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if db_activity and db_activity.is_active:
        if db_activity.capacity is None or db_activity.registered_count < db_activity.capacity:
            db_activity.registered_count += 1
            db.commit()
            db.refresh(db_activity)
            return True
    return False