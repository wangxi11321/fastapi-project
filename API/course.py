from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session
from typing import Optional, List
from FastAPI项目.db_model.database import get_db
from FastAPI项目.pydantic_model.course import CourseCreate, CourseUpdate, CourseResponse, CoursePageResponse, CourseBatchCreate
from FastAPI项目.dao_model import course
from FastAPI项目.common.schemas import success_response, fail_response, page_response


course_router = APIRouter(prefix="/api/course")


@course_router.get("/courses", summary="查询课程列表")
def get_course_list(
    db: Session = Depends(get_db),
    page: int = Query(1, gt=0, description="页码"),
    page_size: int = Query(5, gt=0, description="每页条数"),
    course_name: Optional[str] = Query(None, description="课程名称模糊搜索"),
    show_deleted: bool = Query(False, description="是否显示已删除")
):
    if show_deleted:
        data = course.get_deleted_course_list(db, (page - 1) * page_size, page_size)
        total = course.count_deleted_course(db)
    else:
        data = course.get_course_list(db, (page - 1) * page_size, page_size, course_name)
        total = course.count_course(db)
    
    return page_response(data=data, total=total, page=page, page_size=page_size)


@course_router.get("/courses/{course_id}", summary="查询单个课程")
def get_course(course_id: int = Path(gt=0, description="课程ID"), db: Session = Depends(get_db)):
    result = course.get_course_by_course_id(db, course_id)
    if result:
        return success_response(data=result)
    return fail_response(msg="课程不存在")


@course_router.post("/courses", summary="创建课程")
def create_course(data: CourseCreate, db: Session = Depends(get_db)):
    if course.get_course_by_course_id(db, data.course_id):
        return fail_response(msg="课程ID已存在")
    
    if not data.course_name or not data.course_name.strip():
        return fail_response(msg="课程名称不能为空")
    
    result = course.create_course(db, data)
    return success_response(msg="创建成功", data=result)


@course_router.post("/courses/batch", summary="批量创建课程")
def batch_create_course(data: CourseBatchCreate, db: Session = Depends(get_db)):
    if not data.courses or len(data.courses) == 0:
        return fail_response(msg="课程列表不能为空")
    
    for item in data.courses:
        if course.get_course_by_course_id(db, item.course_id):
            return fail_response(msg=f"课程ID {item.course_id} 已存在")
    
    result = course.batch_create_course(db, data.courses)
    return success_response(msg="批量创建成功", data=result)


@course_router.put("/courses/{course_id}", summary="更新课程")
def update_course(course_id: int = Path(gt=0, description="课程ID"), 
                  data: CourseUpdate = Depends(), 
                  restore: bool = Query(False, description="是否恢复已删除课程"),
                  db: Session = Depends(get_db)):
    if restore:
        result = course.restore_course(db, course_id)
        if not result:
            return fail_response(msg="要恢复的课程不存在或未被删除")
        restored_data = course.get_course_by_course_id(db, course_id)
        return success_response(msg="恢复成功", data=restored_data)
    
    update_data = data.model_dump(exclude_unset=True)
    if not course.update_course(db, course_id, update_data):
        return fail_response(msg="要修改的课程不存在")
    
    updated_data = course.get_course_by_course_id(db, course_id)
    return success_response(msg="更新成功", data=updated_data)


@course_router.delete("/courses/{course_id}", summary="删除课程")
def delete_course(course_id: int = Path(gt=0, description="课程ID"), db: Session = Depends(get_db)):
    if not course.delete_course(db, course_id):
        return fail_response(msg="要删除的课程不存在")
    return success_response(msg="删除成功")
