# 沃林学生管理系统

基于 FastAPI 构建的学生管理系统，提供完整的学生、课程、成绩、就业等信息管理功能。

## 项目架构

```
FastAPI项目/
├── API/                    # 路由层 - REST API 接口定义
│   ├── student.py          # 学生管理接口
│   ├── course.py           # 课程管理接口
│   ├── department.py       # 部门管理接口
│   ├── employee.py         # 员工管理接口
│   ├── classes_api.py      # 班级管理接口
│   ├── score_info_api.py   # 成绩管理接口
│   ├── employement.py      # 就业信息接口
│   └── analys_api.py       # 统计分析接口
├── dao_model/              # 数据访问层 - 数据库操作
│   ├── student.py          # 学生数据操作
│   ├── course.py           # 课程数据操作
│   ├── department.py       # 部门数据操作
│   ├── classes_dao.py      # 班级数据操作
│   ├── score.py            # 成绩数据操作
│   ├── employee_crud.py    # 员工数据操作
│   └── employment.py       # 就业数据操作
├── pydantic_model/         # 数据验证层 - 请求/响应模型
│   ├── student.py          # 学生模型
│   ├── course.py           # 课程模型
│   ├── department.py       # 部门模型
│   └── score_pdmd.py       # 成绩模型
├── table_model/            # 数据库模型层 - ORM 映射
│   ├── dim_stu.py          # 学生表
│   ├── dim_course.py       # 课程表
│   ├── dim_class.py        # 班级表
│   ├── dim_department.py   # 部门表
│   ├── dim_employees.py    # 员工表
│   ├── score_info.py       # 成绩表
│   └── employment_info.py  # 就业表
├── db_model/               # 数据库配置层
│   ├── config.py           # 数据库配置
│   └── database.py         # 数据库连接
├── common/                 # 公共模块
│   └── exception_handler.py # 异常处理
├── frontend/               # 前端页面
│   ├── index.html          # 首页
│   ├── css/styles.css      # 样式文件
│   └── js/                 # JavaScript 文件
├── main.py                 # 项目入口
├── requirements.txt        # 依赖列表
├── .env                    # 环境变量配置
└── .gitignore              # Git 忽略配置
```

## 技术栈

| 分类 | 技术 | 版本 |
|------|------|------|
| 语言 | Python | 3.10+ |
| 框架 | FastAPI | 0.109.0 |
| 数据库 | SQLite / MySQL | - |
| ORM | SQLAlchemy | 2.0+ |
| 数据验证 | Pydantic | 2.0+ |
| 服务器 | Uvicorn | 0.27.0 |

## 功能模块

| 模块 | 功能 | 状态 |
|------|------|------|
| 👨‍🎓 学生管理 | 学生信息的增删改查 | ✅ |
| 📚 课程管理 | 课程信息的增删改查 | ✅ |
| 🏠 班级管理 | 班级信息管理 | ✅ |
| 🏢 部门管理 | 部门信息管理 | ✅ |
| 👔 员工管理 | 员工信息管理 | ✅ |
| 📝 成绩管理 | 考试成绩管理 | ✅ |
| 💼 就业管理 | 就业信息管理 | ✅ |
| 📈 统计分析 | 数据统计分析 | ✅ |

## 快速开始

### 环境要求

- Python 3.10+
- SQLite（内置，无需额外安装）或 MySQL 5.7+

### 安装依赖

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 配置环境变量

编辑 `.env` 文件配置数据库连接：

```env
# 数据库类型: sqlite 或 mysql
DB_TYPE=sqlite

# SQLite 配置
DATABASE_URL=sqlite:///./fastapi.db

# MySQL 配置（使用 MySQL 时取消注释）
# DB_HOST=127.0.0.1
# DB_PORT=3306
# DB_USER=root
# DB_PASS=your_password
# DB_NAME=fastapi
```

### 初始化数据库

```bash
# SQLite 初始化
python init_sqlite.py

# MySQL 初始化（需要先安装 MySQL）
# python init_database.py
```

### 启动服务

```bash
# 开发模式
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000

# 生产模式
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

## 访问地址

| 地址 | 说明 |
|------|------|
| http://localhost:8000/ | 前端页面 |
| http://localhost:8000/docs | API 文档（Swagger UI） |
| http://localhost:8000/redoc | API 文档（ReDoc） |
| http://localhost:8000/api | 后端 API 接口 |

## API 接口

### 学生管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /students | 获取学生列表 |
| GET | /students/{stu_id} | 获取单个学生 |
| POST | /students | 创建学生 |
| PUT | /students/{stu_id} | 更新学生 |
| DELETE | /students/{stu_id} | 删除学生 |

### 课程管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/course/courses | 获取课程列表 |
| GET | /api/course/course/{course_id} | 获取课程详情 |
| POST | /api/course/courses | 创建课程 |
| PUT | /api/course/course/update/{course_id} | 更新课程 |
| DELETE | /api/course/course/delete/{course_id} | 删除课程 |

### 班级管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /classes/classes | 获取班级列表 |
| GET | /classes/classes/{class_id} | 获取班级详情 |
| POST | /classes/classes | 创建班级 |
| PUT | /classes/{class_id} | 更新班级 |
| DELETE | /classes/classes/{class_id} | 删除班级 |

### 成绩管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /score/get_all | 获取所有成绩 |
| GET | /score/{stu_id} | 获取学生成绩 |
| POST | /score/ | 添加成绩 |
| PUT | /score/update | 更新成绩 |
| DELETE | /score/delete | 删除成绩 |

### 统计分析

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /statistics/high_score | 高分学生 |
| GET | /statistics/low_score | 低分学生 |
| GET | /statistics/avg_score | 班级平均分 |
| GET | /statistics/statistics/top5-salary | 薪资TOP5 |

## 数据库管理

项目提供了数据库管理工具：

```bash
python db_manager.py
```

功能包括：
1. 查看所有表
2. 查看表结构
3. 查询表数据
4. 执行SQL语句

## 目录结构说明

| 目录 | 职责 | 说明 |
|------|------|------|
| API/ | 路由层 | 定义 REST API 端点 |
| dao_model/ | 数据访问层 | 封装数据库 CRUD 操作 |
| pydantic_model/ | 数据验证层 | 请求/响应数据结构定义 |
| table_model/ | 数据库模型层 | SQLAlchemy ORM 模型 |
| db_model/ | 配置层 | 数据库连接和配置 |
| common/ | 公共模块 | 异常处理等通用功能 |
| frontend/ | 前端页面 | HTML/CSS/JavaScript |

## 开发规范

### 代码风格

- 使用 PEP 8 代码规范
- 使用类型注解
- 函数/方法注释使用 docstring

### 提交规范

```
feat: 添加新功能
fix: 修复 bug
docs: 更新文档
style: 代码格式调整
refactor: 代码重构
test: 测试相关
chore: 构建/工具相关
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

如有问题，请联系项目维护者。
