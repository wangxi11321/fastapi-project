# Pydantic 模型层：校验前后端传的数据 写 Pydantic 数据校验模型
from  datetime  import date
from pydantic import BaseModel, Field
from typing import Optional
# =====================  学生新增请求体（用于【新增接口】接收前端参数） =====================
class StudentCreate(BaseModel):
    # 核心必填字段
    stu_name: str = Field(..., description="学生姓名（必填）")
    class_id: int = Field(..., description="班级ID（必填）")
    stu_id: int = Field(..., description="学生ID（必填，DAO层用到）")

    # 可选字段
    gender: Optional[str] = Field(None, description="性别")
    age: Optional[int] = Field(None, description="年龄")
    major: Optional[str] = Field(None, description="专业")
    advisor_id: Optional[int] = Field(None, description="导师ID（外键依赖）")
    course_id: Optional[int] = Field(None, description="课程ID（外键依赖）")
    hometown: Optional[str] = Field(None, description="籍贯")
    graduate_school: Optional[str] = Field(None, description="毕业院校")
    education: Optional[str] = Field(None, description="学历")
    stu_flag: Optional[str] = Field(None, description="学生状态标识")
    enroll_time: Optional[date] = Field(None, description="入学时间")
    graduate_time: Optional[date] = Field(None, description="毕业时间")


    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


# ===================== 单个学生信息响应子模型（所有接口返回学生数据时复用） =====================
class StudentInfo(BaseModel):
    """单个学生的详细信息模型（和DAO层返回字段一一对应）"""
    stu_id: Optional[int] = Field(None, description="学生ID")
    stu_name: Optional[str] = Field(None, description="学生姓名")
    gender: Optional[str] = Field(None, description="性别")
    age: Optional[int] = Field(None, description="年龄")
    class_id: Optional[int] = Field(None, description="班级ID")
    major: Optional[str] = Field(None, description="专业")
    advisor_id: Optional[int] = Field(None, description="导师ID")
    course_id: Optional[int] = Field(None, description="课程ID")
    hometown: Optional[str] = Field(None, description="籍贯")
    graduate_school: Optional[str] = Field(None, description="毕业院校")
    education: Optional[str] = Field(None, description="学历")
    stu_flag: Optional[str] = Field(None, description="学生状态标识")
    enroll_time: Optional[str] = Field(None, description="入学时间（格式：YYYY-MM-DD）")
    graduate_time: Optional[str] = Field(None, description="毕业时间（格式：YYYY-MM-DD）")

    class Config:
        from_attributes = True
# =====================  通用新增响应体（用于【新增接口】返回数据） =====================
class StudentResponse(BaseModel):
    """学生新增接口的统一响应体模型"""
    status: str = Field(..., description="请求状态：success/fail")
    msg: str = Field(..., description="提示信息")
    data: Optional[StudentInfo] = Field(None, description="新增的学生信息")  # 返回单个新增的学生数据

    class Config:
        from_attributes = True
        extra = "allow"
