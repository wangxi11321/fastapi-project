from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import customers, reports, leaves, feedback, activities, tools

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="留学机构智能助手平台 API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(customers.router, prefix="/api/customers", tags=["意向客户"])
app.include_router(reports.router, prefix="/api/reports", tags=["日报管理"])
app.include_router(leaves.router, prefix="/api/leaves", tags=["请假申请"])
app.include_router(feedback.router, prefix="/api/feedback", tags=["售后反馈"])
app.include_router(activities.router, prefix="/api/activities", tags=["活动管理"])
app.include_router(tools.router, prefix="/api/tools", tags=["Dify工具"])

@app.get("/")
async def root():
    return {"message": "留学机构智能助手平台 API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}