#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
留学机构智能助手平台 - 简化启动脚本
不依赖可选组件（celery、weasyprint等）
"""
import os
import sys
import logging

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ai_companion")

try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    import uvicorn
    
    logger.info("✓ 核心依赖加载成功")
except ImportError as e:
    logger.error(f"✗ 缺少核心依赖: {e}")
    logger.error("请先安装: pip install fastapi uvicorn")
    sys.exit(1)

app = FastAPI(
    title="留学机构智能助手平台",
    description="企业级AI中台架构 - 简化演示版",
    version="2.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "欢迎使用留学机构智能助手平台",
        "version": "2.0.0",
        "architecture": "AI中台架构",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": __import__('datetime').datetime.now().isoformat()
    }

@app.get("/ready")
async def readiness_check():
    """就绪检查"""
    return {
        "status": "ready",
        "service": "AI中台服务",
        "version": "2.0.0"
    }

@app.get("/api/demo")
async def demo_endpoint():
    """演示API - 展示架构分层"""
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

# 尝试加载完整API（如果依赖可用）
try:
    # 简化版本不加载完整API，避免依赖问题
    logger.info("✅ 简化版本启动成功")
except Exception as e:
    logger.warning(f"⚠️  完整API加载失败: {e}")

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("留学机构智能助手平台 - AI中台架构 v2.0.0")
    logger.info("=" * 60)
    logger.info("📱 API文档地址: http://127.0.0.1:8000/docs")
    logger.info("🏥 健康检查: http://127.0.0.1:8000/health")
    logger.info("🚀 演示API: http://127.0.0.1:8000/api/demo")
    logger.info("=" * 60)
    
    uvicorn.run(
        "start_simple:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
