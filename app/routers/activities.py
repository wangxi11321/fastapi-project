from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.activities import create_activity, get_activity, get_activities, update_activity, register_activity
from app.schemas.activities import ActivityCreate, ActivityUpdate, ActivityResponse, ActivityRegisterRequest
from typing import List

router = APIRouter()

@router.post("/", response_model=ActivityResponse)
def create_activity_endpoint(activity: ActivityCreate, db: Session = Depends(get_db)):
    db_activity = create_activity(db=db, activity=activity)
    return db_activity

@router.get("/", response_model=List[ActivityResponse])
def read_activities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    activities = get_activities(db, skip=skip, limit=limit)
    return activities

@router.get("/{activity_id}", response_model=ActivityResponse)
def read_activity(activity_id: int, db: Session = Depends(get_db)):
    db_activity = get_activity(db, activity_id=activity_id)
    if db_activity is None:
        raise HTTPException(status_code=404, detail="活动不存在")
    return db_activity

@router.put("/{activity_id}", response_model=ActivityResponse)
def update_activity_endpoint(activity_id: int, activity: ActivityUpdate, db: Session = Depends(get_db)):
    db_activity = update_activity(db, activity_id=activity_id, activity_update=activity)
    if db_activity is None:
        raise HTTPException(status_code=404, detail="活动不存在")
    return db_activity

@router.post("/register")
def register_for_activity(request: ActivityRegisterRequest, db: Session = Depends(get_db)):
    success = register_activity(db, activity_id=request.activity_id)
    if not success:
        raise HTTPException(status_code=400, detail="活动已满或不存在")
    return {"message": "报名成功"}