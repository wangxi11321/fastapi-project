from sqlalchemy import Column, Integer, String, Date
from FastAPI项目.db_model.database import Base

class DimDepartment(Base):
    __tablename__ = "dim_department"
    id = Column(Integer,primary_key=True)
    department_id = Column(Integer)
    department_name = Column(String(100))
    create_time = Column(Date)
    end_time = Column(Date)
    deleted_flag = Column(Integer,default=0, comment="0未删除 1已删除")
    insert_date = Column(Date)