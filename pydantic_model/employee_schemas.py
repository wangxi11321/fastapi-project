from datetime import date
from pydantic import BaseModel
from typing import Optional



class EmployeeCreate(BaseModel):
    employee_id: int
    employee_name: str
    position_name: str
    salary: int
    department_id: str
    hire_time: date


# 局部更新
class EmployeeUpdate(BaseModel):
    employee_id: Optional[int] = None
    employee_name: Optional[str] = None
    position_name: Optional[str] = None
    salary: Optional[int] = None
    department_id: Optional[str] = None
    hire_time: Optional[date] = None

