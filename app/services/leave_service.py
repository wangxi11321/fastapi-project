from sqlalchemy.orm import Session
from datetime import date
from typing import Optional, List, Dict, Any
from app.models.leave_applications import LeaveApplication
from app.schemas.leave_applications import LeaveApplicationCreate, LeaveApplicationUpdate
from app.crud.leave_applications import (
    create_leave_application,
    get_leave_application,
    get_leave_applications_by_student,
    get_leave_applications_by_status,
    update_leave_application,
    delete_leave_application
)
from app.ai.workflows.leave_workflow import LeaveWorkflow
from app.core.logger import logger

class LeaveService:
    def __init__(self, db: Session):
        self.db = db
        self.workflow = LeaveWorkflow(db)

    def create_leave_application(self, leave_data: LeaveApplicationCreate) -> LeaveApplication:
        logger.info(f"Creating leave application for {leave_data.student_name}")
        db_leave = create_leave_application(self.db, leave_data)
        logger.info(f"Leave application created: {db_leave.id}")
        return db_leave

    def get_leave_application(self, leave_id: int) -> Optional[LeaveApplication]:
        return get_leave_application(self.db, leave_id)

    def get_leave_applications_by_student(self, student_id: int) -> List[LeaveApplication]:
        return get_leave_applications_by_student(self.db, student_id)

    def get_leave_applications_by_status(self, status: str) -> List[LeaveApplication]:
        return get_leave_applications_by_status(self.db, status)

    def update_leave_application(self, leave_id: int, update_data: LeaveApplicationUpdate) -> Optional[LeaveApplication]:
        logger.info(f"Updating leave application: {leave_id}")
        return update_leave_application(self.db, leave_id, update_data)

    def delete_leave_application(self, leave_id: int) -> bool:
        logger.info(f"Deleting leave application: {leave_id}")
        return delete_leave_application(self.db, leave_id)

    def apply_leave(self, leave_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Processing leave application for {leave_data.get('student_name')}")
        result = self.workflow.execute_application(leave_data)
        return result

    def approve_leave(self, leave_id: int, approver_id: int, approver_name: str, comment: str = "") -> Optional[LeaveApplication]:
        logger.info(f"Approving leave application: {leave_id} by {approver_name}")
        update_data = LeaveApplicationUpdate(
            status="approved",
            approver_id=approver_id,
            approver_name=approver_name,
            approve_comment=comment
        )
        return update_leave_application(self.db, leave_id, update_data)

    def reject_leave(self, leave_id: int, approver_id: int, approver_name: str, comment: str = "") -> Optional[LeaveApplication]:
        logger.info(f"Rejecting leave application: {leave_id} by {approver_name}")
        update_data = LeaveApplicationUpdate(
            status="rejected",
            approver_id=approver_id,
            approver_name=approver_name,
            approve_comment=comment
        )
        return update_leave_application(self.db, leave_id, update_data)