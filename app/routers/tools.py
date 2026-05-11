from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, timedelta
from app.core.database import get_db
from app.crud.intent_customers import create_intent_customer, get_intent_customers
from app.crud.daily_reports import create_daily_report, get_daily_reports_by_date, get_daily_reports_by_week
from app.crud.leave_applications import create_leave_application
from app.crud.feedback_tickets import create_feedback_ticket, get_feedback_tickets_by_status
from app.crud.activities import get_activities, register_activity
from app.schemas.intent_customers import IntentCustomerCreate, CustomerJudgeRequest
from app.schemas.daily_reports import DailyReportCreate
from app.schemas.leave_applications import LeaveApplicationCreate
from app.schemas.feedback_tickets import FeedbackTicketCreate
from app.tools.customer_judge import CustomerJudgeTool
from app.tools.report_generator import ReportGeneratorTool
from typing import List, Dict, Any

router = APIRouter()

@router.post("/judge_customer")
def judge_customer(request: CustomerJudgeRequest):
    result = CustomerJudgeTool.judge_customer(request.customer_info, request.file_path)
    return result

@router.post("/judge_and_save_customer")
def judge_and_save_customer(request: CustomerJudgeRequest, db: Session = Depends(get_db)):
    customer_create = CustomerJudgeTool.judge_and_create(request.customer_info)
    db_customer = create_intent_customer(db=db, customer=customer_create)
    return {"customer": db_customer, "judge_result": {"is_target": customer_create.is_target}}

@router.get("/get_customers")
def get_customers(db: Session = Depends(get_db)):
    customers = get_intent_customers(db)
    return [{"id": c.id, "name": c.name, "phone": c.phone, "is_target": c.is_target} for c in customers]

@router.post("/create_daily_report")
def create_report_for_dify(data: Dict[str, Any], db: Session = Depends(get_db)):
    report = DailyReportCreate(
        employee_id=data["employee_id"],
        employee_name=data["employee_name"],
        date=data["date"],
        content=data["content"],
        summary=data.get("summary"),
        tasks_done=data.get("tasks_done"),
        tasks_tomorrow=data.get("tasks_tomorrow"),
        issues=data.get("issues")
    )
    db_report = create_daily_report(db=db, report=report)
    return {"message": "日报创建成功", "id": db_report.id}

@router.get("/daily_summary")
def get_daily_summary_for_dify(report_date: date = None, db: Session = Depends(get_db)):
    if report_date is None:
        report_date = date.today()
    reports = get_daily_reports_by_date(db, report_date=report_date)
    summary = ReportGeneratorTool.generate_daily_summary(reports)
    return {"summary": summary}

@router.get("/weekly_summary")
def get_weekly_summary_for_dify(db: Session = Depends(get_db)):
    today = date.today()
    start_date = today - timedelta(days=today.weekday())
    end_date = start_date + timedelta(days=6)
    reports = get_daily_reports_by_week(db, start_date=start_date, end_date=end_date)
    summary = ReportGeneratorTool.generate_weekly_summary(reports)
    return {"summary": summary}

@router.post("/apply_leave")
def apply_leave_for_dify(data: Dict[str, Any], db: Session = Depends(get_db)):
    leave = LeaveApplicationCreate(
        student_id=data["student_id"],
        student_name=data["student_name"],
        leave_type=data["leave_type"],
        start_date=data["start_date"],
        end_date=data["end_date"],
        reason=data.get("reason")
    )
    db_leave = create_leave_application(db=db, leave=leave)
    return {"message": "请假申请已提交", "id": db_leave.id, "status": db_leave.status}

@router.post("/submit_feedback")
def submit_feedback_for_dify(data: Dict[str, Any], db: Session = Depends(get_db)):
    feedback = FeedbackTicketCreate(
        student_id=data["student_id"],
        student_name=data["student_name"],
        type=data["type"],
        content=data["content"]
    )
    db_feedback = create_feedback_ticket(db=db, feedback=feedback)
    return {"message": "反馈已提交", "id": db_feedback.id}

@router.get("/get_activities")
def get_activities_for_dify(db: Session = Depends(get_db)):
    activities = get_activities(db)
    return [{"id": a.id, "name": a.name, "type": a.type, "location": a.location, "start_date": a.start_date} for a in activities]

@router.post("/register_activity")
def register_activity_for_dify(data: Dict[str, Any], db: Session = Depends(get_db)):
    success = register_activity(db, activity_id=data["activity_id"])
    if success:
        return {"message": "报名成功"}
    else:
        raise HTTPException(status_code=400, detail="活动已满或不存在")

@router.get("/complaint_report")
def get_complaint_report_for_dify(db: Session = Depends(get_db)):
    today = date.today()
    start_date = today - timedelta(days=7)
    tickets = get_feedback_tickets_by_status(db, status="pending")
    report = ReportGeneratorTool.generate_complaint_report(tickets)
    return {"report": report}