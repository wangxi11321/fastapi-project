import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from FastAPI项目.db_model.database import Base,engine
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from FastAPI项目.API import course,department,student,analys_api,score_info_api,classes_api,employee,employement
from FastAPI项目.common.exception_handler import register_exception_handlers


app = FastAPI(title="沃林学生管理系统", version="1.0.0")

# 注册全局异常处理器
register_exception_handlers(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

index_html_path = os.path.join(FRONTEND_DIR, "index.html")
with open(index_html_path, "r", encoding="utf-8") as f:
    HTML_CONTENT = f.read()

app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")

@app.get("/", response_class=HTMLResponse, description="前端页面", summary="前端页面", tags=["前端页面"])
def root():
    return HTML_CONTENT

# 主界面接口
@app.get("/api",description="沃林学生管理系统API",summary="主界面接口",tags=["主界面"])
def first_menu():
    return {"message": "欢迎进入沃林学生管理系统", "api_docs": "/docs"}
# 导入子路由
app.include_router(router=course.course_router,tags=['课程管理模块'])
app.include_router(router=department.department_router,tags=['部门管理模块'])
app.include_router(router=student.router,tags=['学生管理模块'])
app.include_router(router=score_info_api.score_router, prefix="/score",tags=["成绩管理模块"])
app.include_router(router=classes_api.classes_router, prefix="/classes", tags=["班级管理模块"])
app.include_router(router=employee.router,prefix="/employee",tags=["雇员管理模块"])
app.include_router(router=employement.router,tags=["就业信息管理模块"])
app.include_router(router=analys_api.analys_router, prefix="/statistics",tags=["统计分析模块"])


if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
