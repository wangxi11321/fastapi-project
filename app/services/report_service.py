from sqlalchemy.orm import Session
from datetime import date, timedelta
from typing import Optional, List, Dict, Any
from app.models.daily_reports import DailyReport
from app.models.feedback_tickets import FeedbackTicket
from app.schemas.daily_reports import DailyReportCreate, DailyReportUpdate
from app.crud.daily_reports import (
    create_daily_report,
    get_daily_report,
    get_daily_reports_by_date,
    get_daily_reports_by_week,
    update_daily_report,
    delete_daily_report
)
from app.crud.feedback_tickets import get_feedback_tickets_by_status
from app.ai.agents.report_agent import ReportAgent
from app.core.logger import logger

class ReportService:
    def __init__(self, db: Session):
        self.db = db
        self.report_agent = ReportAgent()

    def create_daily_report(self, report_data: DailyReportCreate) -> DailyReport:
        logger.info(f"Creating daily report for {report_data.employee_name}")
        db_report = create_daily_report(self.db, report_data)
        logger.info(f"Daily report created: {db_report.id}")
        return db_report

    def get_daily_report(self, report_id: int) -> Optional[DailyReport]:
        return get_daily_report(self.db, report_id)

    def get_daily_reports_by_date(self, report_date: date) -> List[DailyReport]:
        return get_daily_reports_by_date(self.db, report_date)

    def get_daily_reports_by_week(self, start_date: date, end_date: date) -> List[DailyReport]:
        return get_daily_reports_by_week(self.db, start_date, end_date)

    def update_daily_report(self, report_id: int, update_data: DailyReportUpdate) -> Optional[DailyReport]:
        logger.info(f"Updating daily report: {report_id}")
        return update_daily_report(self.db, report_id, update_data)

    def delete_daily_report(self, report_id: int) -> bool:
        logger.info(f"Deleting daily report: {report_id}")
        return delete_daily_report(self.db, report_id)

    def generate_daily_summary(self, report_date: Optional[date] = None) -> Dict[str, Any]:
        if report_date is None:
            report_date = date.today()
        
        logger.info(f"Generating daily summary for {report_date}")
        reports = self.get_daily_reports_by_date(report_date)
        summary = self.report_agent.generate_daily_summary(reports)
        
        return {
            "date": report_date,
            "summary": summary,
            "report_count": len(reports)
        }

    def generate_weekly_summary(self) -> Dict[str, Any]:
        today = date.today()
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)
        
        logger.info(f"Generating weekly summary: {start_date} ~ {end_date}")
        reports = self.get_daily_reports_by_week(start_date, end_date)
        summary = self.report_agent.generate_weekly_summary(reports)
        
        return {
            "start_date": start_date,
            "end_date": end_date,
            "summary": summary,
            "report_count": len(reports)
        }

    def generate_complaint_report(self) -> Dict[str, Any]:
        today = date.today()
        start_date = today - timedelta(days=7)
        
        logger.info(f"Generating complaint report: {start_date} ~ {today}")
        tickets = get_feedback_tickets_by_status(self.db, status="pending")
        report = self.report_agent.generate_complaint_report(tickets)
        
        return {
            "start_date": start_date,
            "end_date": today,
            "report": report,
            "ticket_count": len(tickets)
        }