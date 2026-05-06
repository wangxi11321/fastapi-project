from datetime import date
from typing import Optional
from pydantic import BaseModel, Field

# 新增就业信息 - 请求模型
class EmploymentAdd(BaseModel):
    class_id: int = Field(..., description="班级ID")
    stu_id: int = Field(..., description="学生ID")
    employment_open_date: Optional[date] = Field(None, description="简历开放时间")
    first_offer_date: Optional[date] = Field(None, description="第一份offer")
    get_offer_num: Optional[int] = Field(None, description="offer数量")
    employment_date: Optional[date] = Field(None, description="就业时间")
    employment_status: Optional[str] = Field(None, description="就业状态", max_length=20)
    employment_company_name: Optional[str] = Field(None, description="就业公司名称", max_length=255)
    company_city: Optional[str] = Field(None, description="公司所在城市", max_length=255)
    company_type: Optional[str] = Field(None, description="企业所处行业", max_length=255)
    job_position: Optional[str] = Field(None, description="就职岗位", max_length=255)
    salary: Optional[float] = Field(None, description="就业薪资")
    creation_date: Optional[date] = Field(None, description="创建时间")
    insert_date: date = Field(default_factory=date.today, description="数据插入时间")

# 修改就业信息 - 请求模型
class EmploymentUpdate(BaseModel):
    employment_open_date: Optional[date] = Field(None)
    first_offer_date: Optional[date] = Field(None)
    get_offer_num: Optional[int] = Field(None)
    employment_date: Optional[date] = Field(None)
    employment_status: Optional[str] = Field(None, max_length=20)
    employment_company_name: Optional[str] = Field(None, max_length=255)
    company_city: Optional[str] = Field(None, max_length=255)
    company_type: Optional[str] = Field(None, max_length=255)
    job_position: Optional[str] = Field(None, max_length=255)
    salary: Optional[float] = Field(None)

# 就业信息 - 响应模型
# 字典或者json的输出类型（将orm的参数类型转成响应对应的输出类型）
class EmploymentInfo_BASEMODEL(BaseModel):
    id: int
    class_id: int
    stu_id: int
    employment_open_date: date | None = Field(default=None, description="简历开放时间")
    first_offer_date: date | None = Field(default=None, description="第一份offer")
    get_offer_num: int | None = Field(default=None, description="offer数量")
    employment_date: date | None = Field(default=None, description="就业时间")
    employment_status: str | None = Field(default=None, description="就业状态")
    employment_company_name:   str | None = Field(default=None, description="就业公司名称")
    company_city: str | None = Field(default=None, description="公司所在城市")
    company_type: str | None = Field(default=None, description="企业所处行业")
    job_position: str | None = Field(default=None, description="就职岗位")
    salary: float | None = Field(default=None, description="就业薪资")
    delete_flag: int
    creation_date: date | None = Field(default=None, description="创建时间")
    insert_date: date | None = Field(default=None, description="数据插入时间")


    model_config = {"from_attributes": True}

# 学生就业时长 返回模型
class StudentDurationResp(BaseModel):
    id: int
    class_id: int
    stu_id: int
    employment_open_date: Optional[date]
    first_offer_date: Optional[date]
    employment_days: Optional[int]

    model_config = {"from_attributes": True}

# 班级平均就业时长 返回模型
class ClassAvgDurationResp(BaseModel):
    class_id: int
    student_count: int
    avg_employment_days: float

    model_config = {"from_attributes": True}