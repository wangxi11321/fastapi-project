from pydantic import BaseModel,Field
from typing import Optional, List  # 传入字段可传可不传 不传默认是None
from datetime import date

# 创建课程的请求体 所有字段都必传
class CourseCreate(BaseModel):
    # 用 ... 表示必传
    course_id: int = Field(..., description="课程ID（纯数字）")
    # 用 ... 表示必传 并限制长度（和数据库varchar(255)对齐）
    course_name: str = Field(..., description="课程名称", max_length=255)
    # 不传自动生成当前时间
    create_time: date = Field(default_factory=date.today, description="创建日期")
    # 默认9999-12-31
    end_time: date = Field(default=date(9999, 12, 31), description="失效时间，默认永久有效")
    # 不传默认是0，传了也只能传0 和 1
    deleted_flag: int = Field(0, ge=0, le=1, description="删除标识 0-未删除 1-已删除")
    insert_date: date = Field(default_factory=date.today, description="数据插入时间")

# 更新课程信息的请求体 所有字段可以选择传 只传要修改的字段
class CourseUpdate(BaseModel):
      # 限制长度
      course_name: Optional[str] = Field(None, description="课程名称", max_length=255)
      create_time: Optional[date] = Field(None, description="创建日期")
      end_time: Optional[date] = Field(None, description="失效时间")
      # 只能传0 和 1
      deleted_flag: Optional[int] = Field(None, ge=0, le=1, description="删除标识 0-未删除 1-已删除")


# 返回课程信息的响应体
class CourseResponse(BaseModel):
    id: int = Field(description="主键ID")
    course_id: int = Field(description="课程ID")
    course_name: str = Field(description="课程名称")
    create_time: date = Field(description="创建时间")  # 改名为 creation_date
    end_time: Optional[date] = Field(None, description="失效时间，默认9999-12-31")  # 改名为 end_date
    deleted_flag: int = Field(ge=0, le=1, description="删除标识 0-未删除 1-已删除")  # 修正为 deleted_flag
    insert_date: date = Field(description="数据插入时间")
    model_config = {
        "from_attributes": True
    }

# 课程分页响应体
class CoursePageResponse(BaseModel):
    total: int = Field(description="总条数")
    page: int = Field(description="当前页码")
    page_size: int = Field(description="每页条数")
    data: List[CourseResponse] = Field(description="课程列表")

# 批量创建课程的请求体
class CourseBatchCreate(BaseModel):
    courses: List[CourseCreate] = Field(description="课程列表")