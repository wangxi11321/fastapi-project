from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.daily_reports import DailyReport
from app.schemas.daily_reports import DailyReportCreate, DailyReportUpdate
from datetime import date
from typing import Optional, List

def create_daily_report(db: Session, report: DailyReportCreate) -> DailyReport:
    db_report = DailyReport(**report.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

def get_daily_report(db: Session, report_id: int) -> Optional[DailyReport]:
    return db.query(DailyReport).filter(DailyReport.id == report_id).first()

def get_daily_reports_by_employee(db: Session, employee_id: int, skip: int = 0, limit: int = 100) -> List[DailyReport]:
    return db.query(DailyReport).filter(DailyReport.employee_id == employee_id).offset(skip).limit(limit).all()

def get_daily_reports_by_date(db: Session, report_date: date) -> List[DailyReport]:
    return db.query(DailyReport).filter(DailyReport.date == report_date).all()

def get_daily_reports_by_week(db: Session, start_date: date, end_date: date) -> List[DailyReport]:
    return db.query(DailyReport).filter(DailyReport.date >= start_date, DailyReport.date <= end_date).all()

def get_all_daily_reports(db: Session, skip: int = 0, limit: int = 100) -> List[DailyReport]:
    return db.query(DailyReport).offset(skip).limit(limit).all()

def update_daily_report(db: Session, report_id: int, report_update: DailyReportUpdate) -> Optional[DailyReport]:
    db_report = db.query(DailyReport).filter(DailyReport.id == report_id).first()
    if db_report:
        update_data = report_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_report, key, value)
        db.commit()
        db.refresh(db_report)
    return db_report

def delete_daily_report(db: Session, report_id: int) -> bool:
    db_report = db.query(DailyReport).filter(DailyReport.id == report_id).first()
    if db_report:
        db.delete(db_report)
        db.commit()
        return True
    return False