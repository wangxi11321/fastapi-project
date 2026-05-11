from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.core.database import get_db
from app.crud.daily_reports import create_daily_report, get_daily_report, get_daily_reports_by_employee, get_daily_reports_by_date, get_daily_reports_by_week
from app.schemas.daily_reports import DailyReportCreate, DailyReportResponse
from app.tools.report_generator import ReportGeneratorTool
from typing import List

router = APIRouter()

@router.post("/", response_model=DailyReportResponse)
def create_report(report: DailyReportCreate, db: Session = Depends(get_db)):
    db_report = create_daily_report(db=db, report=report)
    return db_report

@router.get("/{report_id}", response_model=DailyReportResponse)
def read_report(report_id: int, db: Session = Depends(get_db)):
    db_report = get_daily_report(db, report_id=report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="日报不存在")
    return db_report

@router.get("/employee/{employee_id}", response_model=List[DailyReportResponse])
def read_reports_by_employee(employee_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reports = get_daily_reports_by_employee(db, employee_id=employee_id, skip=skip, limit=limit)
    return reports

@router.get("/date/{report_date}")
def get_daily_summary(report_date: date, db: Session = Depends(get_db)):
    reports = get_daily_reports_by_date(db, report_date=report_date)
    summary = ReportGeneratorTool.generate_daily_summary(reports)
    return {"summary": summary}

@router.get("/weekly/{start_date}/{end_date}")
def get_weekly_summary(start_date: date, end_date: date, db: Session = Depends(get_db)):
    reports = get_daily_reports_by_week(db, start_date=start_date, end_date=end_date)
    summary = ReportGeneratorTool.generate_weekly_summary(reports)
    return {"summary": summary}