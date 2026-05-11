from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session
from typing import Optional, List
from FastAPI项目.db_model.database import get_db
from FastAPI项目.pydantic_model.department import DepartmentCreate, DepartmentUpdate, DepartmentResponse, DepartmentPageResponse, DepartmentBatchCreate
from FastAPI项目.dao_model import department
from FastAPI项目.common.schemas import success_response, fail_response, page_response


department_router = APIRouter(prefix="/api/department")


@department_router.get("/departments", summary="查询部门列表")
def get_department_list(
    db: Session = Depends(get_db),
    page: int = Query(1, gt=0, description="页码"),
    page_size: int = Query(5, gt=0, description="每页条数"),
    department_name: Optional[str] = Query(None, description="部门名称模糊搜索"),
    show_deleted: bool = Query(False, description="是否显示已删除")
):
    if show_deleted:
        data = department.get_deleted_department_list(db, (page - 1) * page_size, page_size)
        total = department.count_deleted_department(db)
    else:
        data = department.get_department_list(db, (page - 1) * page_size, page_size, department_name)
        total = department.count_department(db)
    
    return page_response(data=data, total=total, page=page, page_size=page_size)


@department_router.get("/departments/{department_id}", summary="查询单个部门")
def get_department(department_id: int = Path(gt=0, description="部门ID"), db: Session = Depends(get_db)):
    result = department.get_department_by_department_id(db, department_id)
    if result:
        return success_response(data=result)
    return fail_response(msg="部门不存在")


@department_router.post("/departments", summary="创建部门")
def create_department(data: DepartmentCreate, db: Session = Depends(get_db)):
    if department.get_department_by_department_id(db, data.department_id):
        return fail_response(msg="部门ID已存在")
    
    if not data.department_name or not data.department_name.strip():
        return fail_response(msg="部门名称不能为空")
    
    result = department.create_department(db, data)
    return success_response(msg="创建成功", data=result)


@department_router.post("/departments/batch", summary="批量创建部门")
def batch_create_department(data: DepartmentBatchCreate, db: Session = Depends(get_db)):
    if not data.departments or len(data.departments) == 0:
        return fail_response(msg="部门列表不能为空")
    
    for item in data.departments:
        if department.get_department_by_department_id(db, item.department_id):
            return fail_response(msg=f"部门ID {item.department_id} 已存在")
    
    result = department.batch_create_department(db, data.departments)
    return success_response(msg="批量创建成功", data=result)


@department_router.put("/departments/{department_id}", summary="更新部门")
def update_department(department_id: int = Path(gt=0, description="部门ID"), 
                      data: DepartmentUpdate = Depends(), 
                      restore: bool = Query(False, description="是否恢复已删除部门"),
                      db: Session = Depends(get_db)):
    if restore:
        result = department.restore_department(db, department_id)
        if not result:
            return fail_response(msg="要恢复的部门不存在或未被删除")
        restored_data = department.get_department_by_department_id(db, department_id)
        return success_response(msg="恢复成功", data=restored_data)
    
    update_data = data.model_dump(exclude_unset=True)
    if not department.update_department(db, department_id, update_data):
        return fail_response(msg="要修改的部门不存在")
    
    updated_data = department.get_department_by_department_id(db, department_id)
    return success_response(msg="更新成功", data=updated_data)


@department_router.delete("/departments/{department_id}", summary="删除部门")
def delete_department(department_id: int = Path(gt=0, description="部门ID"), db: Session = Depends(get_db)):
    if not department.delete_department(db, department_id):
        return fail_response(msg="要删除的部门不存在")
    return success_response(msg="删除成功")
