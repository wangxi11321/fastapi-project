# -*- coding: utf-8 -*-
# 全局自定义异常工具类
from fastapi import HTTPException

# 数据不存在 404
def not_found_exception(msg: str = "记录不存在"):
    """统一抛出数据不存在异常"""
    raise HTTPException(status_code=404, detail=msg)

# 请求参数错误 400
def bad_request_exception(msg: str = "请求参数非法"):
    """统一抛出参数错误异常"""
    raise HTTPException(status_code=400, detail=msg)

# 无权限 403
def forbidden_exception(msg: str = "暂无操作权限"):
    raise HTTPException(status_code=403, detail=msg)

# 服务器内部错误 500
def server_error_exception(msg: str = "服务器内部异常，请稍后重试"):
    """统一抛出服务端错误异常"""
    raise HTTPException(status_code=500, detail=msg)