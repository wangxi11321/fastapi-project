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

# 创建子路由对象，统一管理学生相关接口
router = APIRouter(
    prefix="/students"
)
# ===================== 无条件查询，返回固定字段(带分页)=====================
@router.get("",  summary="获取所有学生列表（固定字段）")
def list_students(
        page: int = 1,   # 页码，默认第1页
        size: int = 10,  # 每页条数，默认10条
    db: Session = Depends(get_db) # 依赖注入，自动获取数据库连接
):# 调用DAO层函数，获取学生简单列表
    return Read_simple_student_dao(db, page, size)

# ===================== 获取单个学生信息 =====================
@router.get("/{stu_id}", summary="获取单个学生信息（支持姓名模糊+班级查询）")# 请求参数查询
def get_student(   #根据学号查询单个学生，支持附加条件：姓名模糊查询、班级编号，漏洞：必选主键与筛选条件中可能存在逻辑冲突
    stu_id: int,                # 必传：学生编号
    stu_name: str = None,      # 可选：姓名模糊
    class_id: int = None,      # 可选：班级编号
    db: Session = Depends(get_db) # 获取数据库会话
):
    # 调用DAO层，传入查询条件，返回单个学生详情
    return Read_student_dao(db, stu_name, stu_id, class_id)

# =====================  新增学生 =====================
@router.post("", summary="创建新学生")
# 功能：添加新学生，接收完整学生信息
def create_student(stu: StudentCreate, db: Session = Depends(get_db)):
    # 调用DAO层执行新增操作
    dao_result = add_student_dao(db, stu)
    try:
        # 判断DAO返回状态，成功则返回成功信息
        if dao_result["status"] == "success":
            return {
                "code": 200,
                "msg": dao_result["msg"],
                "stu_id": dao_result["data"]["stu_id"],
                "name": dao_result["data"]["stu_name"]
            }
        else:
            # 业务失败返回500
            return {"code": 500, "msg": dao_result["msg"], "stu_id": None, "name": None}
    except Exception as e:
        # 系统异常捕获
        return {"code": 500, "msg": f"新增失败：{str(e)}", "stu_id": None, "name": None}

# =====================  逻辑删除学生 =====================
@router.delete("/{stu_id}", summary="学生逻辑删除")
def delete_student(stu_id: int, db: Session = Depends(get_db)):
    # 调用DAO执行删除
    dao_result = del_student_dao(db, stu_id)
    try:
        if dao_result["status"] == "success":
            return {
                "code": 200,
                "msg": dao_result["msg"],
                "stu_id": dao_result["data"]["stu_id"],
                "name": dao_result["data"]["stu_name"]
            }
        else:
            return {"code": 500, "msg": dao_result["msg"], "stu_id": None, "name": None}
    except Exception as e:
        return {"code": 500, "msg": f"删除异常：{str(e)}", "stu_id": None, "name": None}

# =====================  修改学生 =====================
@router.put("/{stu_id}", summary="更新学生信息")
def update_student(stu_id: int, stu: StudentCreate, db: Session = Depends(get_db)):
    # 调用DAO执行更新
    dao_result = update_student_dao(db, stu_id, stu)
    try:
        if dao_result["status"] == "success":
            return {
                "code": 200,
                "msg": dao_result["msg"],
                "stu_id": dao_result["data"]["stu_id"],
                "name": dao_result["data"]["stu_name"]
            }
        else:
            return {"code": 500, "msg": dao_result["msg"], "stu_id": None, "name": None}
    except Exception as e:
        return {"code": 500, "msg": f"修改异常：{str(e)}", "stu_id": None, "name": None}

