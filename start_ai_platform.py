#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
留学机构智能助手平台 - 启动脚本
企业级 AI 中台架构 v2.0.0
"""

import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.logger import logger

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("留学机构智能助手平台 - AI中台架构 v2.0.0")
    logger.info("=" * 60)
    
    try:
        import uvicorn
        
        logger.info("正在启动 FastAPI 服务器...")
        logger.info("API文档地址: http://127.0.0.1:8000/docs")
        logger.info("健康检查地址: http://127.0.0.1:8000/health")
        logger.info("准备就绪检查: http://127.0.0.1:8000/ready")
        logger.info("=" * 60)
        
        uvicorn.run(
            "app.main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except ImportError as e:
        logger.error(f"缺少依赖包: {e}")
        logger.error("请先安装依赖: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        logger.error(f"启动失败: {e}")
        sys.exit(1)
