from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session
from typing import List
from FastAPI项目.pydantic_model.employment import EmploymentInfo_BASEMODEL, EmploymentAdd, EmploymentUpdate
from FastAPI项目.dao_model.employment import create_employment, get_employment_by_student, get_employment_by_class, update_employment, delete_employment, get_all_employment
from FastAPI项目.db_model.database import get_db
from FastAPI项目.common.schemas import success_response, fail_response


router = APIRouter(prefix="/employment")


@router.get("/", summary="查询就业信息列表")
def get_all(db: Session = Depends(get_db), 
            stu_id: int = Query(None, description="学生ID筛选"),
            class_id: int = Query(None, description="班级ID筛选")):
    if stu_id:
        result = get_employment_by_student(db, stu_id)
    elif class_id:
        result = get_employment_by_class(db, class_id)
    else:
        result = get_all_employment(db)
    
    if result:
        return success_response(data=result)
    return fail_response(msg="未查询到就业信息")


@router.get("/{stu_id}", summary="查询单个学生就业信息")
def get_by_student(stu_id: int = Path(gt=0, description="学生ID"), db: Session = Depends(get_db)):
    result = get_employment_by_student(db, stu_id)
    if result:
        return success_response(data=result)
    return fail_response(msg="未查询到该学生的就业信息")


@router.post("/", summary="新增就业信息")
def create(data: EmploymentAdd, db: Session = Depends(get_db)):
    result = create_employment(db, data)
    return success_response(msg="添加成功", data=result)


@router.put("/{stu_id}", summary="更新就业信息")
def update(stu_id: int = Path(gt=0, description="学生ID"), 
           data: EmploymentUpdate = Depends(), 
           db: Session = Depends(get_db)):
    res = update_employment(db, stu_id, data)
    if res:
        return success_response(msg="修改成功", data=res)
    return fail_response(msg="未找到该学生的就业信息")


@router.delete("/{stu_id}", summary="删除就业信息")
def delete(stu_id: int = Path(gt=0, description="学生ID"), db: Session = Depends(get_db)):
    res = delete_employment(stu_id, db)
    if res:
        return success_response(msg="删除成功")
    return fail_response(msg="未找到该学生的就业信息")
