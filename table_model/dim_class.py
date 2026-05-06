from sqlalchemy import Column, Integer, String, Date
from FastAPI项目.db_model.database import Base
from datetime import date


class DimClass(Base):
    __tablename__ = "dim_class"
    id = Column(Integer, primary_key=True, autoincrement=True)  #id,主键，自增
    class_id = Column(Integer,nullable=False)   #班级id,非空
    class_name = Column(String(255))     #班级名称
    class_star_date = Column(Date)  #开班时间
    class_end_date = Column(Date,default='9999-12-31')   #结课时间，默认赋值9999-12-31
    course_id = Column(Integer)  #课程编号
    teacher_id  = Column(Integer)   #授课老师编号
    head_teacher_id = Column(Integer) #班主任编号
    tutor_id = Column(Integer)  #助教编号
    deleted_flag = Column(Integer,default=0)    #有效标识，是否删除（0否1是）默认给0
    insert_date = Column(Date,default = date.today())  #数据插入时间,默认赋值计算机当前日期