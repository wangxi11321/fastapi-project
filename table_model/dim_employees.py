
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from FastAPI项目.db_model.database import Base


class Employees(Base):
    __tablename__ = "dim_employees"

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键id')
    employee_id = Column(Integer, comment='雇员编号')
    employee_name = Column(String(100), comment='雇员名称')
    position_name = Column(String(100), comment='职位名称')
    salary = Column(Integer,comment='薪资')
    create_time = Column(Date, comment='创建时间')
    department_id = Column(Integer, comment='所属部门id')
    hire_time = Column(Date, comment='入职时间')
    end_time = Column(Date, comment='失效时间')
    deleted_flag = Column(Integer, default=0, comment='是否删除 0否1是')
    insert_date = Column(Date, comment='数据插入时间')

    # classes = relationship(
    #     "Class",
    #     primaryjoin="foreign(Class.teacher_id) == Employees.employee_id",
    #     back_populates="teacher",
    #     viewonly = True
    # )