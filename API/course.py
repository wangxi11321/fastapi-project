from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from FastAPI项目.db_model.database import get_db
from FastAPI项目.pydantic_model.course import CourseCreate, CourseUpdate, CourseResponse, CoursePageResponse, CourseBatchCreate
from FastAPI项目.dao_model import course
import re

course_router = APIRouter(prefix="/api/course")
# 创建课程
@course_router.post("/courses"
                    , response_model=CourseResponse
                    , summary="创建课程")
def create_course(data: CourseCreate
               , db: Session = Depends(get_db)): # 依赖注入

    # 验证课程ID是否为数字
    if not isinstance(data.course_id, (int, float)):
        raise HTTPException(status_code=400, detail="课程ID必须为数字")
    # 验证课程ID是否为非负
    # if data.course_id < 0:
    #     raise HTTPException(status_code=400, detail="课程ID不能为负数")
    # 验证课程ID是否为正整数
    if not float(data.course_id).is_integer() or data.course_id <= 0:
        raise HTTPException(status_code=400, detail="课程ID必须为正整数")
    # 验证课程ID是否已存在
    if course.get_course_by_course_id(db, data.course_id):
        raise HTTPException(status_code=400, detail="课程ID已存在")
    # 验证课程名称不能为空
    if not data.course_name or not data.course_name.strip():
        raise HTTPException(status_code=400, detail="课程名称不能为空")
    # 验证课程名称不能包含特殊字符
    if re.search(r'[<>\'\"\\/]', data.course_name):
        raise HTTPException(status_code=400, detail="课程名称不能包含特殊字符")
    return course.create_course(db, data)

# 批量创建课程
@course_router.post("/courses/batch"
                    , response_model=List[CourseResponse]
                    , summary="批量创建课程")
def batch_create_course(data: CourseBatchCreate
                     , db: Session = Depends(get_db)):
    # 验证列表不能为空
    if not data.courses or len(data.courses) == 0:
        raise HTTPException(status_code=400, detail="课程列表不能为空")
    # 验证每个课程的数据
    for item in data.courses:
        # 验证课程ID是否为数字
        if not isinstance(item.course_id, (int, float)):
            raise HTTPException(status_code=400, detail=f"课程ID {item.course_id} 必须为数字")
        # 验证课程ID是否为正整数
        if not float(item.course_id).is_integer() or item.course_id <= 0:
            raise HTTPException(status_code=400, detail=f"课程ID {item.course_id} 必须为正整数")
        # 验证课程ID是否已存在
        if course.get_course_by_course_id(db, item.course_id):
            raise HTTPException(status_code=400, detail=f"课程ID {item.course_id} 已存在")
        # 验证课程名称不能为空
        if not item.course_name or not item.course_name.strip():
            raise HTTPException(status_code=400, detail=f"课程名称不能为空")
        # 验证课程名称不能包含特殊字符
        if re.search(r'[<>\'\"\\/]', item.course_name):
            raise HTTPException(status_code=400, detail=f"课程名称不能包含特殊字符")
    # 批量创建
    return course.batch_create_course(db, data.courses)

# 通过指定课程id查询单个
@course_router.get("/course/{course_id}"
                    , response_model=CourseResponse
                    ,summary="查询单个课程") # 单个数据返回的响应体
def get_course(course_id: int
            , db: Session = Depends(get_db)):
    # 验证课程ID是否为数字
    if not isinstance(course_id, (int, float)):
        raise HTTPException(status_code=400, detail="课程ID必须为数字")
    # 验证课程ID是否为非负
    # if course_id < 0:
    #     raise HTTPException(status_code=400, detail="课程ID不能为负数")
    # 验证课程ID是否为正整数
    if not float(course_id).is_integer() or course_id <= 0:
        raise HTTPException(status_code=400, detail="课程ID必须为正整数")
    # 验证课程ID是否存在
    result = course.get_course_by_course_id(db, course_id)
    # 找不到要查询的课程 返回404-课程不存在
    if not result:
        raise HTTPException(status_code=404, detail="课程不存在")
    return result

# 分页查询课程列表
@course_router.get("/courses"
                    , response_model=CoursePageResponse
                    , summary="分页查询课程")
def get_course_list(
    db: Session = Depends(get_db),
    page: int = 1,
    page_size: int = 5,
    course_name: Optional[str] = None
):
    # 验证页码是否为数字
    if not isinstance(page, (int, float)):
        raise HTTPException(status_code=400, detail="页码必须为数字")
    # 验证页码是否为正整数
    if not float(page).is_integer() or page <= 0:
        raise HTTPException(status_code=400, detail="页码必须为正整数")
    # 验证条数是否为数字
    if not isinstance(page_size, (int, float)):
        raise HTTPException(status_code=400, detail="每页条数必须为数字")
    # 验证条数是否为正整数
    if not float(page_size).is_integer() or page_size <= 0:
        raise HTTPException(status_code=400, detail="每页条数必须为正整数")
    skip = (page - 1) * page_size
    data = course.get_course_list(db, skip, page_size, course_name)
    total = course.count_course(db)
    return CoursePageResponse(total=total, page=page, page_size=page_size, data=data)

# 修改课程信息
@course_router.put("/course/update/{course_id}",summary="修改课程信息") # 根据指定课程ID更新课程
def update_course(
    course_id: int,
    data: CourseUpdate, # 更新数据的请求体
    db: Session = Depends(get_db)

):
    # 验证课程ID是否为数字
    if not isinstance(course_id, (int, float)):
        raise HTTPException(status_code=400, detail="课程ID必须为数字")
    # 验证课程ID是否为非负
    # if course_id < 0:
    #     raise HTTPException(status_code=400, detail="课程ID不能为负数")
    # 验证课程ID是否为正整数
    if not float(course_id).is_integer() or course_id <= 0:
        raise HTTPException(status_code=400, detail="课程ID必须为正整数")
    update_data = data.model_dump(exclude_unset=True)
    # 验证要修改的课程名称不能为空
    if 'course_name' in update_data:
        if not update_data['course_name'] or not update_data['course_name'].strip():
            raise HTTPException(status_code=400, detail="课程名称不能为空")
        if re.search(r'[<>\'\"\\/]', update_data['course_name']):
            raise HTTPException(status_code=400, detail="课程名称不能包含特殊字符")
    # 找不到要更新的课程 返回404-课程不存在
    if not course.update_course(db, course_id, update_data):
        raise HTTPException(status_code=404, detail="要修改的课程不存在")
    # 返回更新后的完整数据
    updated_data = course.get_course_by_course_id(db, course_id)
    return {"message": "更新成功", "data": updated_data}

# 根据课程ID删除课程 只对删除标识进行修改 不删除数据
@course_router.delete("/course/delete/{course_id}",summary="删除课程(软删除)") # 根据指定课程ID删除课程
def delete_course(course_id: int
                , db: Session = Depends(get_db)):
    # 验证课程ID是否为数字
    if not isinstance(course_id, (int, float)):
        raise HTTPException(status_code=400, detail="课程ID必须为数字")
    # 验证课程ID是否为非负
    # if course_id < 0:
    #     raise HTTPException(status_code=400, detail="课程ID不能为负数")
    # 验证课程ID是否为正整数
    if not float(course_id).is_integer() or course_id <= 0:
        raise HTTPException(status_code=400, detail="课程ID必须为正整数")
    # 找不到要删除的课程 返回404-课程不存在
    if not course.delete_course(db, course_id):
        raise HTTPException(status_code=404, detail="要删除的课程不存在")
    return {"message": "删除成功"}

# 恢复误删的课程（撤回）
@course_router.put("/course/restore/{course_id}", summary="恢复误删课程")
def restore_course(course_id: int, db: Session = Depends(get_db)):
    if not float(course_id).is_integer() or course_id <= 0:
        raise HTTPException(status_code=400, detail="课程ID必须为正整数")
    result = course.restore_course(db, course_id)
    if not result:
        raise HTTPException(status_code=404, detail="要恢复的课程不存在或未被删除")
    restored_course = course.get_course_by_course_id(db, course_id)
    return {"message": "恢复成功", "data": restored_course}

# 查询已删除的课程列表（可恢复列表）
@course_router.get("/courses/deleted", summary="查询已删除课程列表")
def get_deleted_courses(
    db: Session = Depends(get_db),
    page: int = 1,
    page_size: int = 10
):
    skip = (page - 1) * page_size
    data = course.get_deleted_course_list(db, skip, page_size)
    total = course.count_deleted_course(db)
    return {"total": total, "page": page, "page_size": page_size, "data": data}

