#就业信息明细表 dwd_employment_info_detail
from sqlalchemy import Integer, Column, String, Date, Float
from FastAPI项目.db_model.database import Base

class EmploymentInfo(Base):
    # 指定当前类对应的数据库真实表名
    __tablename__ = "dwd_employment_info_detail"
    id = Column(Integer, primary_key=True, autoincrement=True)# 主键ID：自增、唯一标识
    class_id = Column(Integer)#班级编号
    stu_id = Column(Integer)#学生编号
    employment_open_date = Column(Date, nullable=True)#就业开放时间
    first_offer_date = Column(Date, nullable=True)#第一次拿offer的时间,空值不报错
    get_offer_num = Column(Integer, nullable=True)#获得offer数量
    employment_date = Column(Date, nullable=True)#就业时间
    employment_status = Column("mployment_status", String(20), nullable=True)#就业状态
    employment_company_name = Column(String(255), nullable=True)#就业公司名称
    company_city = Column(String(255), nullable=True)#公司所在城市
    company_type = Column(String(255), nullable=True)#企业所处行业
    job_position = Column(String(255), nullable=True)#就职岗位
    salary = Column(Float, nullable=True)#就业薪资
    delete_flag = Column(Integer, default=0, comment="是否删除 0否1是")
    creation_date = Column(Date, nullable=True)#创建时间
    insert_date = Column(Date, nullable=True)#数据插入时间