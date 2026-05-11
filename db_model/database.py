"""
数据库相关
数据库连接及引擎会话
"""
from sqlalchemy import create_engine # 创建数据库连接的工具
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker # 创建数据库会话的工具
from FastAPI项目.db_model import config # 数据库url

#创建数据库引擎
engine = create_engine(config.DATABASE_URL) # 相当于打开 Python 和 MySQL 之间的 “桥梁 / 通道”

#创建会话类
SessionLocal = sessionmaker(bind=engine) # 每次要操作数据库，就从这里造一个新会话

#引入ORM基类
Base = declarative_base() # ORM 模型的基类（父类）

#数据库依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()