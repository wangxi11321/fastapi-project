# 留学机构智能助手平台 (AI Companion System)

基于 FastAPI + Dify 构建的留学机构智能助手平台，提供客户研判、客服Agent、企业智能助手、学生智能助手和智能报告等核心功能。

## 技术架构

```
用户端（微信/企业微信/网页）
         ↓ (HTTP / WebSocket)
 [Dify Applications] ←→ [Dify Knowledge Base]
         ↓
 [自定义 Python Tools] ←→ [FastAPI Backend]
         ↓
 PostgreSQL + Redis + Vector DB
```

## 功能模块

| 模块 | 功能 |
|------|------|
| **客户研判** | 自动判断客户是否符合目标客户画像 |
| **客服Agent** | 公司信息咨询、留学政策查询、课程推荐等 |
| **企业智能助手** | 意向客户管理、日报生成与查询 |
| **学生智能助手** | 请假申请、学业进度查询、售后反馈 |
| **智能报告** | 日报/周报汇总、投诉处理报告 |

## 项目结构

```
app/
├── main.py              # FastAPI主应用
├── core/                # 配置与数据库连接
│   ├── config.py        # 环境配置
│   └── database.py      # 数据库连接
├── models/              # SQLAlchemy模型
│   ├── intent_customers.py
│   ├── daily_reports.py
│   ├── leave_applications.py
│   ├── feedback_tickets.py
│   └── activities.py
├── schemas/             # Pydantic Schema
├── crud/                # CRUD操作
├── routers/             # API路由
├── tools/               # Dify自定义工具
│   ├── customer_judge.py
│   └── report_generator.py
└── utils/               # 工具函数
    └── file_parser.py
```

## 快速开始

### 环境要求

- Python 3.11+
- PostgreSQL 15+
- Redis 7+

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置环境变量

复制 `.env` 文件并修改配置：

```bash
cp .env.example .env
```

### 数据库迁移

```bash
alembic upgrade head
```

### 运行服务

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 使用 Docker

```bash
docker-compose up -d
```

## API文档

启动服务后访问：
- Swagger UI: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

## Dify工具接口

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/tools/judge_customer` | POST | 客户画像研判 |
| `/api/tools/judge_and_save_customer` | POST | 研判并保存客户 |
| `/api/tools/get_customers` | GET | 查询意向客户列表 |
| `/api/tools/create_daily_report` | POST | 创建日报 |
| `/api/tools/daily_summary` | GET | 获取日报汇总 |
| `/api/tools/weekly_summary` | GET | 获取周报汇总 |
| `/api/tools/apply_leave` | POST | 提交请假申请 |
| `/api/tools/submit_feedback` | POST | 提交售后反馈 |
| `/api/tools/get_activities` | GET | 获取活动列表 |
| `/api/tools/register_activity` | POST | 活动报名 |
| `/api/tools/complaint_report` | GET | 获取投诉处理报告 |

## 许可证

MIT License