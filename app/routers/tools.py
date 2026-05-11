from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, timedelta
from app.core.database import get_db
from app.services.customer_service import CustomerService
from app.services.report_service import ReportService
from app.services.leave_service import LeaveService
from app.crud.feedback_tickets import create_feedback_ticket, get_feedback_tickets_by_status
from app.crud.activities import get_activities, register_activity
from app.schemas.intent_customers import CustomerJudgeRequest
from app.schemas.feedback_tickets import FeedbackTicketCreate
from typing import List, Dict, Any

router = APIRouter()

def get_customer_service(db: Session = Depends(get_db)) -> CustomerService:
    return CustomerService(db)

def get_report_service(db: Session = Depends(get_db)) -> ReportService:
    return ReportService(db)

def get_leave_service(db: Session = Depends(get_db)) -> LeaveService:
    return LeaveService(db)

@router.post("/judge_customer")
def judge_customer(
    request: CustomerJudgeRequest,
    service: CustomerService = Depends(get_customer_service)
):
    result = service.judge_and_create_customer(request.customer_info)
    return result

@router.post("/judge_and_save_customer")
def judge_and_save_customer(
    request: CustomerJudgeRequest,
    service: CustomerService = Depends(get_customer_service)
):
    result = service.judge_and_create_customer(request.customer_info)
    return {
        "customer_created": result.get("customer_created", False),
        "customer_id": result.get("customer_id"),
        "judge_result": {
            "is_target": result.get("is_target", False),
            "reason": result.get("reason")
        }
    }

@router.get("/get_customers")
def get_customers(service: CustomerService = Depends(get_customer_service)):
    customers = service.get_customers()
    return [{"id": c.id, "name": c.name, "phone": c.phone, "is_target": c.is_target} for c in customers]

@router.post("/create_daily_report")
def create_report_for_dify(
    data: Dict[str, Any],
    service: ReportService = Depends(get_report_service)
):
    from app.schemas.daily_reports import DailyReportCreate
    
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
    db_report = service.create_daily_report(report)
    return {"message": "日报创建成功", "id": db_report.id}

@router.get("/daily_summary")
def get_daily_summary_for_dify(
    report_date: date = None,
    service: ReportService = Depends(get_report_service)
):
    result = service.generate_daily_summary(report_date)
    return {"summary": result["summary"]}

@router.get("/weekly_summary")
def get_weekly_summary_for_dify(service: ReportService = Depends(get_report_service)):
    result = service.generate_weekly_summary()
    return {"summary": result["summary"]}

@router.post("/apply_leave")
def apply_leave_for_dify(
    data: Dict[str, Any],
    service: LeaveService = Depends(get_leave_service)
):
    result = service.apply_leave(data)
    return result

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
def get_complaint_report_for_dify(service: ReportService = Depends(get_report_service)):
    result = service.generate_complaint_report()
    return {"report": result["report"]}