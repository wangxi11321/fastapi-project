from sqlalchemy import and_, func
from sqlalchemy.orm import Session, joinedload
from datetime import date
from FastAPI项目.table_model.dim_employees import Employees
from FastAPI项目.table_model.dim_class import DimClass
from FastAPI项目.pydantic_model.employee_schemas import EmployeeCreate, EmployeeUpdate


# 查询所有员工
def get_all_employees(db: Session):
    return db.query(Employees).all()


# 根据名字模糊查询
def search_employee(db: Session, employee_name: str = None):
    # 查询条件是在职状态的员工
    q = db.query(Employees).filter(and_(Employees.deleted_flag == 0))
    if employee_name:
        q = q.filter(Employees.employee_name.like(f"%{employee_name}%"))
    return q.all()


# 通过id查询员工
def get_one_employee(db: Session, id: int):
    return db.query(Employees).filter(and_(Employees.id == id)).first()


# 新增员工信息
def create_employee(db: Session, data: EmployeeCreate):
    exist = db.query(Employees).filter(and_(
        Employees.employee_id == data.employee_id,
        Employees.deleted_flag == 0
    )).first()
    # 如果重复，直接返回 None
    if exist:
        return None
    emp = Employees(
        employee_id=data.employee_id,
        employee_name=data.employee_name,
        position_name=data.position_name,
        salary=data.salary,
        department_id=data.department_id,
        hire_time=data.hire_time,
        create_time=date.today(),
        insert_date=date.today(),
        deleted_flag=0
    )
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp


# 删除
def delete_employee(db: Session, employee_id: int):
    emp = db.query(Employees).filter(and_(Employees.employee_id == employee_id,
                                          Employees.deleted_flag == 0)).first()
    if not emp:
        return None
    emp.deleted_flag = 1  # 0是存在状态，1是不存在状态
    db.commit()
    db.refresh(emp)
    return emp


# 局部添加员工信息
# 修改
def update_employee(db: Session, employee_id: int, data: EmployeeUpdate):
    emp = db.query(Employees).filter(and_(Employees.employee_id == employee_id,
                                          Employees.deleted_flag == 0)).first()
    if not emp:
        return None
    # data.dict()把pydantic模型转成字典"exclude_unsett=True"只保留前端传了的字段，没传的字段直接丢掉
    update_data = data.dict(exclude_unset=True, exclude_none=True)
    for key, value in update_data.items():
        setattr(emp, key, value)
    db.commit()
    db.refresh(emp)
    return emp


# 统计在职员工总人数，平均薪资，最高最低工资
def get_employee_count(db: Session):
    #  在职总人数
    total_employees = (db.query(func.count(Employees.employee_id))
                       .filter(and_(Employees.deleted_flag == 0)).scalar())
    #  在职员工薪资统计
    avg_salary = ((db.query(func.avg(Employees.salary)))
                  .filter(and_(Employees.deleted_flag == 0)).scalar())
    max_salary = ((db.query(func.max(Employees.salary)))
                  .filter(and_(Employees.deleted_flag == 0)).scalar())
    min_salary = ((db.query(func.min(Employees.salary)))
                  .filter(and_(Employees.deleted_flag == 0)).scalar())
    return {
        "在职员工总人数": total_employees,
        "平均薪资": round(avg_salary, 2),
        "最高工资": round(max_salary, 2),
        "最低工资": round(min_salary, 2)
    }


# 统计每个职称人数
def get_employee_by_position(db: Session):
    res = (db.query(Employees.position_name,
                    func.count(Employees.employee_id).label("职位人数"))
           .filter(and_(Employees.deleted_flag == 0))
           .group_by(Employees.position_name).all())
    return [{"职位名称": i[0], "职位人数": i[1]} for i in res]


# 连接班级表查询
def get_emp_with_class_by_id(db: Session, employee_id: int):
    employee = (db.query(Employees)
                .filter(and_(Employees.employee_id == employee_id,
                             Employees.deleted_flag == 0))).first()
    if not employee:
        return None
    class_list = (db.query(DimClass)
                  .filter(and_(DimClass.teacher_id == employee.employee_id,
                               Employees.deleted_flag == 0, ))).all()
    employee.classes = class_list
    return employee
    # 使用 joinedload 查询员工时不管有没有班级
    # return db.query(Employees).options(joinedload(Employees.classes)).filter(
    #     and_(Employees.employee_id == employee_id,
    #          Employees.deleted_flag == 0)).first()


