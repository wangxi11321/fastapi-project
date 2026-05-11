from typing import Dict, Any
from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.crud.leave_applications import create_leave_application
from app.schemas.leave_applications import LeaveApplicationCreate
from app.core.logger import logger

class LeaveWorkflow:
    def __init__(self, db: Session):
        self.db = db

    def execute_application(self, leave_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Starting leave application workflow")
        
        try:
            validation_result = self._validate_leave(leave_data)
            
            if not validation_result["valid"]:
                return {
                    "success": False,
                    "status": "rejected",
                    "reason": validation_result["reason"]
                }
            
            leave_record = self._create_leave_application(leave_data)
            
            if self._auto_approve(leave_data):
                return {
                    "success": True,
                    "status": "approved",
                    "id": leave_record.id,
                    "reason": "自动审批通过"
                }
            
            self._notify_manager(leave_record)
            
            return {
                "success": True,
                "status": "pending",
                "id": leave_record.id,
                "reason": "已提交审批"
            }
            
        except Exception as e:
            logger.error(f"Leave application workflow failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "status": "failed"
            }

    def _validate_leave(self, data: Dict[str, Any]) -> Dict[str, Any]:
        required_fields = ["student_id", "student_name", "leave_type", "start_date", "end_date"]
        
        for field in required_fields:
            if field not in data:
                return {"valid": False, "reason": f"缺少必填字段: {field}"}
        
        try:
            start_date = date.fromisoformat(data["start_date"])
            end_date = date.fromisoformat(data["end_date"])
            
            if start_date > end_date:
                return {"valid": False, "reason": "开始日期不能晚于结束日期"}
            
            duration = (end_date - start_date).days + 1
            
            if duration > 30:
                return {"valid": False, "reason": "单次请假不能超过30天"}
            
            return {"valid": True, "reason": "验证通过"}
            
        except ValueError as e:
            return {"valid": False, "reason": f"日期格式错误: {e}"}

    def _create_leave_application(self, data: Dict[str, Any]) -> Any:
        leave_create = LeaveApplicationCreate(
            student_id=data["student_id"],
            student_name=data["student_name"],
            leave_type=data["leave_type"],
            start_date=date.fromisoformat(data["start_date"]),
            end_date=date.fromisoformat(data["end_date"]),
            reason=data.get("reason")
        )
        
        return create_leave_application(self.db, leave_create)

    def _auto_approve(self, data: Dict[str, Any]) -> bool:
        try:
            start_date = date.fromisoformat(data["start_date"])
            end_date = date.fromisoformat(data["end_date"])
            duration = (end_date - start_date).days + 1
            
            return duration <= 1
        except Exception:
            return False

    def _notify_manager(self, leave_record: Any):
        logger.info(f"Notifying manager about leave application {leave_record.id}")