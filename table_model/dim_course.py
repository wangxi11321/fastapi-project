from sqlalchemy import Column, Integer, String, Date
from FastAPI项目.db_model.database import Base
from datetime import date

class DimCourse(Base):
    __tablename__ = "dim_course"
    # 主键
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    # 补充唯一约束（课程ID应唯一）
    course_id = Column(Integer, comment="课程编号，唯一", unique=True)
    # 补充非空约束（课程名称必传）
    course_name = Column(String(255), comment="课程名称", nullable=False)
    create_time = Column(Date, default=date.today, comment="创建时间", nullable=False)
    end_time = Column(Date, default=date(9999, 12, 31), comment="失效时间，默认永久有效", nullable=False)
    deleted_flag = Column(Integer,default=0,comment="删除标识 0-未删除 1-已删除")
    insert_date = Column(Date, default=date.today, comment="数据插入/更新时间", nullable=False)
