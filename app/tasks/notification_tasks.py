from celery import shared_task
from app.core.logger import logger

@shared_task
def send_notification(recipient: str, message: str, channel: str = "wechat"):
    try:
        logger.info(f"Sending notification to {recipient} via {channel}: {message}")
        return {"status": "success", "recipient": recipient, "channel": channel}
    except Exception as e:
        logger.error(f"Failed to send notification: {e}")
        return {"status": "failed", "error": str(e)}

@shared_task
def send_daily_report_reminder(employee_ids: list):
    try:
        logger.info(f"Sending daily report reminders to {len(employee_ids)} employees")
        return {"status": "success", "count": len(employee_ids)}
    except Exception as e:
        logger.error(f"Failed to send daily report reminders: {e}")
        return {"status": "failed", "error": str(e)}

@shared_task
def send_leave_approval_notification(student_id: int, leave_id: int, status: str):
    try:
        logger.info(f"Sending leave approval notification for student {student_id}, leave {leave_id}, status {status}")
        return {"status": "success", "student_id": student_id, "status": status}
    except Exception as e:
        logger.error(f"Failed to send leave approval notification: {e}")
        return {"status": "failed", "error": str(e)}