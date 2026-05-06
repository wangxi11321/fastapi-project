from pydantic import BaseModel,Field
from typing import Optional, List  # 传入字段可传可不传 不传默认是None
from datetime import date

# 创建部门信息的请求体 所有字段都必传
class DepartmentCreate(BaseModel):
    # 必须传
    department_id: int = Field(description="部门ID（纯数字）")
    department_name: str = Field(description="部门名称")
    # 不传自动生成当前时间
    create_time: date = Field(default_factory=date.today, description="创建日期")
    # 默认9999-12-31
    end_time: date = Field(default=date(9999, 12, 31), description="失效时间，默认永久有效")
    # 不传默认是0，传了也只能传0 和 1
    deleted_flag: int = Field(0, ge=0, le=1, description="删除标识 0-未删除 1-已删除")
    # 不传自动生成当前时间
    insert_date: date = Field(default_factory=date.today, description="数据插入时间")

# 更新部门信息的请求体 所有字段可以选择传 只传要修改的字段
class DepartmentUpdate(BaseModel):
      # 限制长度
      department_name: Optional[str] = Field(None, description="部门名称",max_length=100)
      create_time: Optional[date] = Field(None, description="创建日期")
      end_time: Optional[date] = Field(None, description="失效时间")
      # 只能传0 和 1
      deleted_flag: Optional[int] = Field(None, ge=0, le=1, description="删除标识 0-未删除 1-已删除")

# 返回部门信息的响应体
class DepartmentResponse(BaseModel):
    id: int = Field(description="主键ID")
    department_id: int = Field(description="部门ID")
    department_name: str = Field(description="部门名称")
    create_time: date = Field(description="创建时间")
    end_time: Optional[date] = Field(None, description="失效时间，默认9999-12-31")
    deleted_flag: int = Field(ge=0, le=1, description="删除标识 0-未删除 1-已删除")
    insert_date: date = Field(description="数据插入时间")
    model_config = {
        "from_attributes": True
    }

# 部门分页响应体
class DepartmentPageResponse(BaseModel):
    total: int = Field(description="总条数")
    page: int = Field(description="当前页码")
    page_size: int = Field(description="每页条数")
    data: List[DepartmentResponse] = Field(description="部门列表")

# 批量创建部门的请求体
class DepartmentBatchCreate(BaseModel):
    departments: List[DepartmentCreate] = Field(description="部门列表")

