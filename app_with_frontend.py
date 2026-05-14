from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
import os

from app.routers.tools import router as tools_router

app = FastAPI(
    title="留学机构智能助手平台",
    description="企业级AI中台架构",
    version="2.0.0"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

index_html_path = os.path.join(FRONTEND_DIR, "index.html")
if os.path.exists(index_html_path):
    with open(index_html_path, "r", encoding="utf-8") as f:
        HTML_CONTENT = f.read()
else:
    HTML_CONTENT = "<h1>Frontend not found</h1>"

app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")
app.include_router(tools_router, prefix="/api/tools", tags=["Tools"])

@app.get("/", response_class=HTMLResponse, description="前端页面")
async def root():
    return HTML_CONTENT

@app.get("/api", description="API信息")
async def api_info():
    return {
        "message": "欢迎使用留学机构智能助手平台",
        "version": "2.0.0",
        "docs": "/docs",
        "architecture": "AI中台架构"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "2.0.0"}

@app.get("/api/demo")
async def demo_api():
    return {
        "layers": [
            "API层 (Routers)",
            "服务层 (Services)", 
            "AI层 (Agents/Workflows/Tools)",
            "数据访问层 (CRUD)",
            "模型层 (Models)"
        ],
        "ai_components": [
            "Agents: 智能代理",
            "Workflows: 工作流引擎",
            "Tools: 工具集",
            "RAG: 知识检索",
            "Prompts: 提示词管理"
        ],
        "business_modules": [
            "客户研判",
            "日报管理", 
            "请假申请",
            "售后反馈",
            "活动管理"
        ]
    }

@app.get("/api/architecture")
async def architecture():
    return {
        "title": "企业级AI中台架构",
        "description": "留学机构智能助手平台采用分层架构设计",
        "layers": {
            "presentation": {
                "name": "展示层",
                "components": ["前端 (React)", "Dify Agent"]
            },
            "api": {
                "name": "API层",
                "components": ["FastAPI Routers", "中间件", "CORS"]
            },
            "service": {
                "name": "服务层",
                "components": ["CustomerService", "ReportService", "LeaveService"]
            },
            "ai": {
                "name": "AI层",
                "components": ["Agents", "Workflows", "Tools", "RAG", "Prompts"]
            },
            "data": {
                "name": "数据层",
                "components": ["CRUD", "Models", "Database", "Vector Store"]
            }
        },
        "features": [
            "关注点分离",
            "Prompt外置管理",
            "工作流引擎",
            "异步任务处理",
            "结构化日志",
            "RAG知识检索"
        ]
    }

if __name__ == "__main__":
    print("=" * 60)
    print("🏛️  留学机构智能助手平台 - AI中台架构 v2.0.0")
    print("=" * 60)
    print("🌐 前端页面: http://127.0.0.1:8000/")
    print("📚 API文档:  http://127.0.0.1:8000/docs")
    print("🏥 健康检查: http://127.0.0.1:8000/health")
    print("🚀 演示API:  http://127.0.0.1:8000/api/demo")
    print("🏗️  架构说明: http://127.0.0.1:8000/api/architecture")
    print("🔧 工具API:  http://127.0.0.1:8000/api/tools/judge_customer_dify")
    print("=" * 60)
    
    uvicorn.run("app_with_frontend:app", host="127.0.0.1", port=8000, reload=True)
