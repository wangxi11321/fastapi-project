from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session
from FastAPI项目.db_model.database import get_db
from FastAPI项目.dao_model.employee_crud import get_all_employees, get_one_employee, create_employee, delete_employee, update_employee, \
     search_employee
from FastAPI项目.pydantic_model.employee_schemas import EmployeeCreate, EmployeeUpdate
from FastAPI项目.common.schemas import success_response, fail_response


router = APIRouter()


@router.get("/employees", summary="查询员工列表")
def list_employees(db: Session = Depends(get_db), 
                   name: str = Query(None, description="姓名模糊搜索")):
    if name:
        data = search_employee(db, name)
    else:
        data = get_all_employees(db)
    
    if data:
        return success_response(data=data)
    return fail_response(msg="未找到员工")


@router.get("/employees/{id}", summary="查询单个员工")
def get_employee_id(id: int = Path(gt=0, description="员工ID"), db: Session = Depends(get_db)):
    emp = get_one_employee(db, id)
    if emp:
        return success_response(data=emp)
    return fail_response(msg="雇员不存在")


@router.post("/employees", summary="新增员工")
def create_emp(data: EmployeeCreate, db: Session = Depends(get_db)):
    emp = create_employee(db, data)
    if emp:
        return success_response(msg="添加成功", data=emp)
    return fail_response(msg="雇员已存在")


@router.put("/employees/{employee_id}", summary="更新员工信息")
def update_emp(employee_id: int = Path(gt=0, description="员工ID"), 
               data: EmployeeUpdate = Depends(), 
               db: Session = Depends(get_db)):
    emp = update_employee(db, employee_id, data)
    if emp:
        return success_response(msg="修改成功", data=emp)
    return fail_response(msg="员工不存在")


@router.delete("/employees/{employee_id}", summary="删除员工")
def del_employee(employee_id: int = Path(gt=0, description="员工ID"), db: Session = Depends(get_db)):
    emp = delete_employee(db, employee_id)
    if emp:
        return success_response(msg="删除成功")
    return fail_response(msg="员工不存在")
