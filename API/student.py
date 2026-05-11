# 导入FastAPI相关依赖：路由、依赖注入
from fastapi import APIRouter, Depends
# 导入数据库会话类
from sqlalchemy.orm import Session
# 导入学生模块的所有DAO层函数（数据访问层，负责数据库操作）
from FastAPI项目.dao_model.student import (
    add_student_dao,
    Read_student_dao,
    del_student_dao,
    update_student_dao,
    Read_simple_student_dao
)
# 导入Pydantic模型，用于接口参数校验（请求体格式）
from FastAPI项目.pydantic_model.student import StudentCreate
# 导入数据库连接依赖（获取数据库会话）
from FastAPI项目.db_model.database import get_db
# 导入统一响应模型和异常处理
from FastAPI项目.common.schemas import ApiResponse, PageResponse, success_response, fail_response, page_response
from FastAPI项目.common.exception_handler import not_found_exception, bad_request_exception

# 创建子路由对象，统一管理学生相关接口
router = APIRouter(
    prefix="/students"
)
# ===================== 无条件查询，返回固定字段(带分页)=====================
@router.get("",  summary="获取所有学生列表（固定字段）", response_model=PageResponse)
def list_students(
        page: int = 1,   # 页码，默认第1页
        page_size: int = 10,  # 每页条数，默认10条
    db: Session = Depends(get_db) # 依赖注入，自动获取数据库会话
):# 调用DAO层函数，获取学生简单列表
    result = Read_simple_student_dao(db, page, page_size)
    if result["status"] == "success":
        return page_response(
            data=result["data"],
            total=result["total"],
            page=page,
            page_size=page_size,
            msg="查询成功"
        )
    else:
        return fail_response(result["msg"])

# ===================== 获取单个学生信息 =====================
@router.get("/{stu_id}", summary="获取单个学生信息（支持姓名模糊+班级查询）", response_model=ApiResponse) # 请求参数查询
def get_student(   #根据学号查询单个学生，支持附加条件：姓名模糊查询、班级编号，漏洞：必选主键与筛选条件中可能存在逻辑冲突
    stu_id: int,                # 必传：学生编号
    stu_name: str = None,      # 可选：姓名模糊
    class_id: int = None,      # 可选：班级编号
    db: Session = Depends(get_db) # 获取数据库会话
):
    # 调用DAO层，传入查询条件，返回单个学生详情
    result = Read_student_dao(db, stu_name, stu_id, class_id)
    if result["status"] == "success":
        if not result["data"]:
            not_found_exception("学生不存在")
        return success_response(data=result["data"], msg="查询成功")
    else:
        return fail_response(result["msg"])

# =====================  新增学生 =====================
@router.post("", summary="创建新学生", response_model=ApiResponse)
# 功能：添加新学生，接收完整学生信息
def create_student(stu: StudentCreate, db: Session = Depends(get_db)):
    # 调用DAO层执行新增操作
    dao_result = add_student_dao(db, stu)
    if dao_result["status"] == "success":
        return success_response(
            data={
                "stu_id": dao_result["data"]["stu_id"],
                "name": dao_result["data"]["stu_name"]
            },
            msg=dao_result["msg"]
        )
    else:
        return fail_response(dao_result["msg"])

# =====================  逻辑删除学生 =====================
@router.delete("/{stu_id}", summary="学生逻辑删除", response_model=ApiResponse)
def delete_student(stu_id: int, db: Session = Depends(get_db)):
    # 调用DAO执行删除
    dao_result = del_student_dao(db, stu_id)
    if dao_result["status"] == "success":
        return success_response(
            data={
                "stu_id": dao_result["data"]["stu_id"],
                "name": dao_result["data"]["stu_name"]
            },
            msg=dao_result["msg"]
        )
    else:
        return fail_response(dao_result["msg"])

# =====================  修改学生 =====================
@router.put("/{stu_id}", summary="更新学生信息", response_model=ApiResponse)
def update_student(stu_id: int, stu: StudentCreate, db: Session = Depends(get_db)):
    # 调用DAO执行更新
    dao_result = update_student_dao(db, stu_id, stu)
    if dao_result["status"] == "success":
        return success_response(
            data={
                "stu_id": dao_result["data"]["stu_id"],
                "name": dao_result["data"]["stu_name"]
            },
            msg=dao_result["msg"]
        )
    else:
        return fail_response(dao_result["msg"])
