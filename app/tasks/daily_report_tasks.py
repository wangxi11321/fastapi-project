from celery import shared_task
from datetime import date
from app.core.logger import logger
from app.services.report_service import ReportService
from app.core.database import SessionLocal

@shared_task
def generate_daily_summary_task(report_date: str = None):
    try:
        db = SessionLocal()
        service = ReportService(db)
        
        if report_date:
            report_date = date.fromisoformat(report_date)
        
        result = service.generate_daily_summary(report_date)
        logger.info(f"Daily summary generated: {result['date']}")
        
        db.close()
        return {"status": "success", "summary_length": len(result["summary"])}
    except Exception as e:
        logger.error(f"Failed to generate daily summary: {e}")
        return {"status": "failed", "error": str(e)}

@shared_task
def generate_weekly_summary_task():
    try:
        db = SessionLocal()
        service = ReportService(db)
        
        result = service.generate_weekly_summary()
        logger.info(f"Weekly summary generated: {result['start_date']} ~ {result['end_date']}")
        
        db.close()
        return {"status": "success", "report_count": result["report_count"]}
    except Exception as e:
        logger.error(f"Failed to generate weekly summary: {e}")
        return {"status": "failed", "error": str(e)}

@shared_task
def generate_complaint_report_task():
    try:
        db = SessionLocal()
        service = ReportService(db)
        
        result = service.generate_complaint_report()
        logger.info(f"Complaint report generated: {result['ticket_count']} tickets")
        
        db.close()
        return {"status": "success", "ticket_count": result["ticket_count"]}
    except Exception as e:
        logger.error(f"Failed to generate complaint report: {e}")
        return {"status": "failed", "error": str(e)}