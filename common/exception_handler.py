# -*- coding: utf-8 -*-
# 全局自定义异常工具类
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError


class BusinessException(Exception):
    """自定义业务异常"""
    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg


# 数据不存在 404
def not_found_exception(msg: str = "记录不存在"):
    """统一抛出数据不存在异常"""
    raise BusinessException(404, msg)


# 请求参数错误 400
def bad_request_exception(msg: str = "请求参数非法"):
    """统一抛出参数错误异常"""
    raise BusinessException(400, msg)


# 无权限 403
def forbidden_exception(msg: str = "暂无操作权限"):
    raise BusinessException(403, msg)


# 服务器内部错误 500
def server_error_exception(msg: str = "服务器内部异常，请稍后重试"):
    """统一抛出服务端错误异常"""
    raise BusinessException(500, msg)


def register_exception_handlers(app: FastAPI):
    """注册全局异常处理器"""

    @app.exception_handler(BusinessException)
    async def business_exception_handler(request: Request, exc: BusinessException):
        """业务异常处理"""
        return JSONResponse(
            status_code=exc.code if 400 <= exc.code < 600 else 500,
            content={
                "code": exc.code,
                "msg": exc.msg,
                "data": None
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """请求参数校验异常处理"""
        return JSONResponse(
            status_code=400,
            content={
                "code": 400,
                "msg": "请求参数错误",
                "data": exc.errors()
            }
        )

    @app.exception_handler(ValidationError)
    async def pydantic_validation_handler(request: Request, exc: ValidationError):
        """Pydantic模型校验异常处理"""
        return JSONResponse(
            status_code=400,
            content={
                "code": 400,
                "msg": "数据格式错误",
                "data": str(exc)
            }
        )

    @app.exception_handler(SQLAlchemyError)
    async def database_exception_handler(request: Request, exc: SQLAlchemyError):
        """数据库异常处理"""
        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "msg": "数据库操作失败",
                "data": str(exc)
            }
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """全局异常捕获"""
        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "msg": f"服务器异常: {str(exc)}",
                "data": None
            }
        )
