# 导入数据库会话对象
from fastapi import Depends
from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from FastAPI项目.common.exception_handler import not_found_exception
from FastAPI项目.db_model.database import get_db
# 导入数据库模型：就业信息表
from FastAPI项目.table_model.employment_info import EmploymentInfo
# 导入schemas数据校验模型
from FastAPI项目.pydantic_model.employment import EmploymentAdd, EmploymentUpdate

# 获取所有就业信息
def get_all_employment(db: Session):
    result = db.query(EmploymentInfo).filter(EmploymentInfo.delete_flag == 0).all()
    return result


# 新增就业信息
# db: 数据库会话
# data: 前端传入的新增参数
def create_employment(db: Session, data: EmploymentAdd):
    # 将前端传入的字典数据，转为数据库模型对象，**表示拆成 key=value 的形式
    db_emp = EmploymentInfo(**data.model_dump())
    # 添加数据到数据库会话
    db.add(db_emp)
    # 提交事务
    db.commit()
    # 刷新数据，获取数据库自动生成一个主键ID
    db.refresh(db_emp)
    # 返回新增完成的数据
    return db_emp

# 根据学生ID查询就业信息
# 只查询未删除数据 delete_flag=0
def get_employment_by_student(db: Session, stu_id: int):
    result = db.query(EmploymentInfo) \
        .filter(and_(EmploymentInfo.stu_id == stu_id,
                EmploymentInfo.delete_flag == 0)).all()
    return result

# 根据班级ID查询就业信息
# 函数的输出类型 orm类型
def get_employment_by_class(db: Session, class_id: int):
    result = db.query(EmploymentInfo) \
        .filter(and_(EmploymentInfo.class_id == class_id,
                EmploymentInfo.delete_flag == 0)).all()
    return result if result is not None else []

# 修改就业信息
# 动态更新前端传递的字段，不传递的字段不修改
def update_employment(db: Session, stu_id: int, data: EmploymentUpdate):
    # 根据id查询单条数据
    emp = db.query(EmploymentInfo).filter(and_(EmploymentInfo.stu_id == stu_id
                                          , EmploymentInfo.delete_flag == 0)).first()
    if not emp:
        not_found_exception("就业信息不存在")
    # 遍历前端传入的字段，动态赋值修改
    for k, v in data.dict(exclude_unset=True).items():
        setattr(emp, k, v)
    # 提交修改
    db.commit()
    db.refresh(emp)
    return emp

# 逻辑删除（软删除）
# 不物理删除数据，只修改删除标记
def delete_employment(stu_id: int, db: Session=Depends(get_db)):
    emp = db.query(EmploymentInfo).filter(and_(EmploymentInfo.stu_id == stu_id, EmploymentInfo.delete_flag == 0)).first()
    if emp:
        emp.delete_flag = 1   # 标记为已删除
        db.commit()           # 提交修改
    return emp

# 薪资倒序TOP5 统计查询
def get_top5_salary(db: Session):
    result = db.query(EmploymentInfo) \
        .filter(EmploymentInfo.salary.isnot(None)) \
        .order_by(EmploymentInfo.salary.desc())\
        .limit(5).all()
    return result

# 统计每个学生就业时长：offer下发时间 - 就业开放时间

def stat_student_duration(db: Session = Depends(get_db)):
    """
    就业时长 = 第一份offer时间 - 就业开放时间
    只统计：有就业开放时间的学生
    """
    emp_list = db.query(EmploymentInfo)\
        .filter(
            and_(EmploymentInfo.delete_flag == 0,
            EmploymentInfo.employment_open_date.isnot(None)
                 )).all()

    res_list = []
    for item in emp_list:
        days = None
        # 两个时间都不为空，再计算差值
        if item.first_offer_date and item.employment_open_date:
            days = (item.first_offer_date - item.employment_open_date).days

        res_list.append({
            "id": item.id,
            "class_id": item.class_id,
            "stu_id": item.stu_id,
            "employment_open_date": item.employment_open_date,
            "first_offer_date": item.first_offer_date,
            "employment_days": days
        })
    return res_list

#统计每个班级 平均就业时长
def stat_class_avg_duration(db: Session = Depends(get_db)):
    """
    筛选条件：
    1. 未删除
    2. 有就业开放时间（进入就业阶段）
    3. 有offer下发时间
    按班级分组，计算平均就业天数
    """
    data = db.query(
        EmploymentInfo.class_id,
        func.count(EmploymentInfo.id).label("student_count"),
        func.avg(
            func.datediff(EmploymentInfo.first_offer_date, EmploymentInfo.employment_open_date)
        ).label("avg_day")
    ).filter(
        and_(EmploymentInfo.delete_flag == 0,
        EmploymentInfo.employment_open_date.isnot(None),
        EmploymentInfo.first_offer_date.isnot(None)
             )).group_by(EmploymentInfo.class_id).all()

    result = []
    for row in data:
        result.append({
            "class_id": row.class_id,
            "student_count": row.student_count,
            "avg_employment_days": round(row.avg_day, 1) if row.avg_day else 0.0
        })

    return result