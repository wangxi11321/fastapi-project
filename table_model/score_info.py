from datetime import date
from sqlalchemy import Column, Integer, Float, Date
from sqlalchemy.sql.expression import text
from FastAPI项目.db_model.database import Base


# 定义学生考试信息明细的数据库模型（建表）
class ScoreInfo(Base):
    # 表名
    __tablename__ = "dwd_score_info_detail"
    # 主键，自增
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    # 与其他表关联的外键
    class_id = Column(Integer, nullable=False, comment="班级ID")
    test_num = Column(Integer, nullable=False, comment="考试序次")
    stu_id = Column(Integer, nullable=False, comment="学生ID")
    exam_course_id = Column(Integer, nullable=False, comment="课程ID")
    # 时间和成绩
    exam_date = Column(Date, nullable=False, comment="考试日期")
    score = Column(Float(2), nullable=False, comment="成绩 0.00~100.00")
    # 删除标记，创建时间，修改时间
    delete_flag = Column(Integer, default=0, server_default=text("0"), nullable=False, comment="删除标记 0未删 1已删")
    creation_date = Column(Date, default=date.today, nullable=False, comment="创建时间")
    insert_date = Column(Date, nullable=False, comment="最后修改时间")
