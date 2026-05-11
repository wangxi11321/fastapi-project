from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.core.database import get_db
from app.services.report_service import ReportService
from app.schemas.daily_reports import DailyReportCreate, DailyReportUpdate, DailyReportResponse
from typing import List

router = APIRouter()

def get_report_service(db: Session = Depends(get_db)) -> ReportService:
    return ReportService(db)

@router.post("/", response_model=DailyReportResponse)
def create_report(
    report: DailyReportCreate,
    service: ReportService = Depends(get_report_service)
):
    db_report = service.create_daily_report(report)
    return db_report

@router.get("/", response_model=List[DailyReportResponse])
def read_reports(
    report_date: date = None,
    service: ReportService = Depends(get_report_service)
):
    if report_date:
        reports = service.get_daily_reports_by_date(report_date)
    else:
        reports = service.get_daily_reports_by_date(date.today())
    return reports

@router.get("/{report_id}", response_model=DailyReportResponse)
def read_report(
    report_id: int,
    service: ReportService = Depends(get_report_service)
):
    db_report = service.get_daily_report(report_id)
    if db_report is None:
        raise HTTPException(status_code=404, detail="日报不存在")
    return db_report

@router.put("/{report_id}", response_model=DailyReportResponse)
def update_report(
    report_id: int,
    report: DailyReportUpdate,
    service: ReportService = Depends(get_report_service)
):
    db_report = service.update_daily_report(report_id, report)
    if db_report is None:
        raise HTTPException(status_code=404, detail="日报不存在")
    return db_report

@router.delete("/{report_id}")
def delete_report(
    report_id: int,
    service: ReportService = Depends(get_report_service)
):
    success = service.delete_daily_report(report_id)
    if not success:
        raise HTTPException(status_code=404, detail="日报不存在")
    return {"message": "日报删除成功"}

@router.get("/summary/daily")
def daily_summary(
    report_date: date = None,
    service: ReportService = Depends(get_report_service)
):
    result = service.generate_daily_summary(report_date)
    return result

@router.get("/summary/weekly")
def weekly_summary(
    service: ReportService = Depends(get_report_service)
):
    result = service.generate_weekly_summary()
    return result

@router.get("/summary/complaint")
def complaint_report(
    service: ReportService = Depends(get_report_service)
):
    result = service.generate_complaint_report()
    return result