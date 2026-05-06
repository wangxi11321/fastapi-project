# 数据库模型层：定义数据库表结构 写 SQLAlchemy ORM 表模型
from sqlalchemy import Date
from sqlalchemy import  Column, Integer, String
from FastAPI项目.db_model.database import  Base

class Student(Base):
    __tablename__ = "dim_stu"
    id = Column(Integer, primary_key=True, autoincrement=True)
    stu_id = Column(Integer)
    stu_name = Column(String(100))
    class_id = Column(Integer)
    gender = Column(String(10))
    age = Column(Integer)
    hometown = Column(String(255))
    graduate_school = Column(String(100))
    major = Column(String(50))
    education = Column(String(50))
    advisor_id = Column(Integer)
    enroll_time = Column(Date)
    graduate_time = Column(Date)
    course_id = Column(Integer)
    stu_flag = Column(String(255))
    deleted_flag = Column(Integer,default=0, comment='是否删除 0否1是')
    create_time = Column(Date)
    end_time = Column(Date)
    insert_date = Column(Date)