from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from FastAPI项目.db_model.database import get_db
from FastAPI项目.dao_model.employee_crud import get_all_employees, get_one_employee, create_employee, delete_employee, update_employee, \
     search_employee
from FastAPI项目.pydantic_model.employee_schemas import EmployeeCreate, EmployeeUpdate

# 子路由
router = APIRouter()


# 查询所有员工信息
@router.get("/employees/employee/list", summary="查询/全部/名字模糊/id精准")
def list_employees(db: Session = Depends(get_db)):
    return get_all_employees(db)


# 根据姓名模糊查询
@router.get("/employees/search", summary="查询/全部/名字模糊/id精准")
def search_employee_name(name: str, db: Session = Depends(get_db)):
    data = search_employee(db, name)
    if not data:
        raise HTTPException(status_code=404, detail="未找到员工")
    return data


# 根据id精准查询
@router.get("/employees/{id}", summary="查询/全部/名字模糊/id精准")
def get_employee_id(id: int, db: Session = Depends(get_db)):
    emp = get_one_employee(db, id)
    if not emp:
        raise HTTPException(status_code=404, detail="雇员不存在")
    return emp


# 添加员工
@router.post("/employees/create_emp", summary="新增员工")
def create_emp(data: EmployeeCreate, db: Session = Depends(get_db)):
    emp = create_employee(db, data)
    if not emp:
        raise HTTPException(status_code=409, detail="雇员已存在")
    return emp


# 根据员工id删除员工
@router.delete("/employees/{employee_id}", summary="删除雇员")
def del_employee(employee_id: int, db: Session = Depends(get_db)):
    emp = delete_employee(db, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="员工不存在")
    return {"message": "已删除"}


# 修改员工信息
@router.put("/employees/{employee_id}", summary="修改员工信息")
def update_emp(employee_id: int, data: EmployeeUpdate, db: Session = Depends(get_db)):
    emp = update_employee(db, employee_id, data)
    if not emp:
        raise HTTPException(status_code=404, detail="员工不存在")
    return emp



