from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from FastAPI项目.pydantic_model.score_pdmd import StatisticsOut
from FastAPI项目.dao_model.score_crud import read_high_score_info, read_low_score_info, read_avg_score_info
from FastAPI项目.db_model.database import get_db
######################################## XZ
from FastAPI项目.dao_model import course
from FastAPI项目.dao_model import department
######################################## WXS
# 导入成绩分析模块的DAO函数
from FastAPI项目.dao_model.score import calc_total_score, get_total_rank, get_subject_rank, get_score_trend
from FastAPI项目.dao_model.student import (
    Read_student_over_30_dao,
    stat_class_gender_dao)
######################################## HHF
from FastAPI项目.dao_model.classes_dao import cls_stu_count, class_sc_avg, class_em_avg
######################################## LB
from FastAPI项目.dao_model.employee_crud import get_employee_count, get_employee_by_position, get_emp_with_class_by_id
######################################## CSX
from FastAPI项目.pydantic_model.employment import EmploymentInfo_BASEMODEL, StudentDurationResp, ClassAvgDurationResp
from typing import List
from FastAPI项目.dao_model.employment import *


analys_router = APIRouter()

########################################################################################### GST
# 查询每次考试成绩都在80分以上的学⽣的编号，姓名和成绩
@analys_router.get("/high_score", response_model=StatisticsOut
                        , response_model_exclude_unset=True
                        ,summary="查询每次考试成绩都在80分以上的学⽣的编号，姓名和成绩")
def get_high_score_info(db: Session = Depends(get_db)):
    result = read_high_score_info(db)
    if result:
        return {"message": "查询成功", "data": result}
    raise HTTPException(status_code=404, detail="未找到")


# 查询有两次以上不及格的学⽣的姓名，班级和不及格成绩
@analys_router.get("/low_score", response_model=StatisticsOut
                    , response_model_exclude_unset=True
                    , summary="查询有两次以上不及格的学⽣的姓名，班级和不及格成绩")
def get_low_score_info(db: Session = Depends(get_db)):
    result = read_low_score_info(db)
    if result:
        return {"message": "查询成功", "data": result}
    raise HTTPException(status_code=404, detail="未找到")


# 统计每次考试每个班级的平均分，按照从⾼到低排序
@analys_router.get("/avg_score", response_model=StatisticsOut
                        , response_model_exclude_unset=True
                        , summary="统计每次考试每个班级的平均分，按照从⾼到低排序")
def get_avg_score_info(db:Session = Depends(get_db)):
    result = read_avg_score_info(db)
    if result:
        return {"message": "查询成功", "data": result}
    raise HTTPException(status_code=404, detail="未找到")

########################################################################## XZ
# 统计有效课程数量
@analys_router.get("/statistics/count_course",summary="统计有效课程数量")
def get_count_course(db: Session = Depends(get_db)):
    return {"message": "查询成功","total_count": course.count_course(db)}

# 统计每门课有多少学生
@analys_router.get("/statistics/count_students_by_course",summary="统计每门课有多少学生")
def get_count_students_by_course(db: Session = Depends(get_db)):
    return course.count_students_by_course(db)

@analys_router.get("/statistics/count_department",summary="统计有效部门数量")
def count_department(db: Session = Depends(get_db)):
    return {"total": department.count_department(db)}

@analys_router.get("/statistics/count_employees_by_department",summary="统计每个部门有多少员工")
def count_employees_by_department(db: Session = Depends(get_db)):
    return department.count_employees_by_department(db)

########################################################################## WXS
# ===================== 6. 年龄>30 =====================
@analys_router.get("/get/over30", summary="查询年龄>30岁学生")
def get_over_30(db: Session = Depends(get_db)):
    # 调用DAO获取年龄>30的学生
    return Read_student_over_30_dao(db)

# ===================== 7. 班级统计 =====================
@analys_router.get("/stat/class", summary="班级人数+男女统计")
def stat_class(db: Session = Depends(get_db)):
    # 调用DAO返回班级统计数据
    return stat_class_gender_dao(db)

# ===================== 8. 成绩分析（4个接口） =====================
@analys_router.get("/analysis/total", summary="计算学生总分")
def api_calc_total(stu_id: int, db: Session = Depends(get_db)):
    return calc_total_score(db, stu_id)

@analys_router.get("/analysis/total-rank", summary="根据学生姓名查询总分排名")
def api_total_rank(
    stu_name: str,  # 接收学生姓名
    db: Session = Depends(get_db)
):
    return get_total_rank(db, stu_name)

@analys_router.get("/analysis/subject-rank", summary="按学生姓名查询：所有科目成绩+单科排名")
def api_subject_rank(
    stu_name: str,  # 只传学生姓名
    db: Session = Depends(get_db)
):
    return get_subject_rank(db, stu_name)

@analys_router.get("/analysis/trend", summary="按姓名查询：每科近5次成绩趋势")
def api_score_trend(
    stu_name: str,  # 只传姓名
    db: Session = Depends(get_db)
):
    return get_score_trend(db, stu_name)
########################################################################################### HHF

#====================================统计管理=========================================
# 统计所有班级人数、男女比例
@analys_router.get("/statistics/classes/count",summary="统计班级人数，男女比例")
def class_student_count(db: Session = Depends(get_db)):
    result = cls_stu_count(db)
    if result:
        return {"message": "查询成功", "data": result}
    raise HTTPException(status_code=404, detail="未查到数据")


# 统计各班每次考试平均分（降序）
@analys_router.get("/statistics/classes/average-score",summary="统计各班每次考试平均分")
def class_avg_score(test_num:int|None = Query(None,alias='考试序次'),db: Session = Depends(get_db)):
    result = class_sc_avg(db,test_num)
    if result:
        return {"message": "成功", "data": result}
    raise HTTPException(status_code=404, detail="未查到数据")


# 统计各班平均就业时长
@analys_router.get("/statistics/classes/average-employment",summary="统计各班平均就业时长")
def class_avg_employment(db: Session = Depends(get_db)):
    result = class_em_avg(db)
    if result:
        return {"message": "查询成功", "data": result}
    raise HTTPException(status_code=404, detail="未查到数据")

########################################################################################### LB
# 统计雇员数量,平均薪资及最高最低薪资
@analys_router.get("/employees/stat/statistics", summary="雇员统计分析")
def get_employee_stats(db: Session = Depends(get_db)):
    emp = get_employee_count(db)
    return emp

# 按职位统计雇员
@analys_router.get("/employees/stat/position", summary="雇员统计分析")
def get_employee_stats_position(db: Session = Depends(get_db)):
    emp = get_employee_by_position(db)
    return emp

# 查询教师所带班级
@analys_router.get("/employees/{employee_id}/class", summary="员工班级关联")
def get_employee_class(employee_id: int, db: Session = Depends(get_db)):
    data = get_emp_with_class_by_id(db, employee_id)
    if not data:
        raise HTTPException(status_code=404, detail="该员工不存在")
    return {"msg": "查询成功", "员工信息及所带班级": data}

########################################################################################### CSX

# 6. 薪资Top5
@analys_router.get("/statistics/top5-salary", response_model=List[EmploymentInfo_BASEMODEL],summary="薪资Top5")
def top5_salary(db: Session = Depends(get_db)):
    return get_top5_salary(db)


# 7. 统计每个学生就业时长：offer下发时间 - 就业开放时间
@analys_router.get("/statistics/student_offer",
            summary="每个学生就业时长",
            response_model=List[StudentDurationResp],
            )
def stat_student_duration1(db: Session = Depends(get_db)):#接口函数和数据函数的函数名称要不一样

    return stat_student_duration(db)

# 8. 统计每个班级 平均就业时长
@analys_router.get("/statistics/avg_student_offer",
            summary="各班平均就业时长",
            response_model=List[ClassAvgDurationResp],
            )
def stat_class_avg_duration2(db: Session = Depends(get_db)):


    return stat_class_avg_duration(db)