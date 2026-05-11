# 统一响应模型
from pydantic import BaseModel, Field
from typing import Optional, TypeVar, Generic, List

T = TypeVar('T')


class ApiResponse(BaseModel, Generic[T]):
    """统一API响应模型"""
    code: int = Field(..., description="响应状态码，200表示成功")
    msg: str = Field(..., description="响应消息")
    data: Optional[T] = Field(None, description="响应数据")

    class Config:
        from_attributes = True


class PageResponse(BaseModel, Generic[T]):
    """分页响应模型"""
    code: int = Field(..., description="响应状态码，200表示成功")
    msg: str = Field(..., description="响应消息")
    total: int = Field(..., description="总条数")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页条数")
    data: Optional[List[T]] = Field(None, description="分页数据列表")

    class Config:
        from_attributes = True


def success_response(data=None, msg="操作成功"):
    """成功响应工厂函数"""
    return ApiResponse(code=200, msg=msg, data=data)


def fail_response(msg="操作失败", code=500):
    """失败响应工厂函数"""
    return ApiResponse(code=code, msg=msg, data=None)


def page_response(data: List, total: int, page: int, page_size: int, msg="查询成功"):
    """分页响应工厂函数"""
    return PageResponse(
        code=200,
        msg=msg,
        total=total,
        page=page,
        page_size=page_size,
        data=data
    )
