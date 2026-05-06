# 导入路由、依赖、异常处理
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
# 导入schemas：请求模型、修改模型、响应模型
from FastAPI项目.pydantic_model.employment import EmploymentInfo_BASEMODEL, EmploymentAdd, EmploymentUpdate
# 导入数据库表模型
from FastAPI项目.table_model.employment_info import EmploymentInfo
# 导入dao层所有增删改查方法
from FastAPI项目.dao_model.employment import *
# 导入全局统一异常工具
from FastAPI项目.common.exception_handler import not_found_exception
# 导入数据库连接
from FastAPI项目.db_model.database import get_db
# 列表返回需要
from typing import List

# 创建路由对象，统一接口前缀、分类标签
router = APIRouter(
    prefix="/employment",   # 所有接口统一前缀

)

# 0. 获取所有就业信息接口
@router.get("/", response_model=List[EmploymentInfo_BASEMODEL],summary="获取所有就业信息")
def get_all(db: Session = Depends(get_db)):
    result = db.query(EmploymentInfo).filter(EmploymentInfo.delete_flag == 0).all()
    return result

# 1. 新增就业信息接口
@router.post("/", response_model=EmploymentInfo_BASEMODEL,summary="新增就业信息接口")
def create(data: EmploymentAdd, db: Session = Depends(get_db)):
    """
    data: 前端传来的新增表单数据
    db: 自动注入数据库会话
    """
    return create_employment(db, data)

# 2. 根据学生ID查询就业信息
@router.get("/students/{stu_id}", response_model=List[EmploymentInfo_BASEMODEL],summary="根据学生ID查询就业信息")
def get_by_student(stu_id: int, db: Session = Depends(get_db)):
    result = get_employment_by_student(db, stu_id)
    return result

# 3. 根据班级ID查询就业信息
@router.get("/class/{class_id}", response_model=List[EmploymentInfo_BASEMODEL],summary="根据班级ID查询就业信息")
def get_by_class(class_id: int, db: Session = Depends(get_db)):
    result = get_employment_by_class(db, class_id) # orm类型的对象result
    return result

# 4. 修改就业信息
@router.put("/students/{id}", response_model=EmploymentInfo_BASEMODEL,summary="修改就业信息")
def update(stu_id: int, data: EmploymentUpdate, db: Session = Depends(get_db)):
    res = update_employment(db, stu_id, data)
    # 统一调用全局异常
    # 判空，找不到数据抛出404异常
    if not res:
        not_found_exception()
    return res

# 5.逻辑删除接口
@router.delete("/students/{id}",summary="逻辑删除")
def delete(stu_id: int, db: Session = Depends(get_db)):
    res = delete_employment(stu_id,db)
    if not res:
        not_found_exception("待删除就业信息")
    return {"msg": "删除成功"}

