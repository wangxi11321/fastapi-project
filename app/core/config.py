import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

class Settings(BaseModel):
    PROJECT_NAME: str = "留学机构智能助手平台"
    DATABASE_URL: str = Field(..., description="数据库连接URL")
    REDIS_URL: str = Field(..., description="Redis连接URL")
    DIFY_API_KEY: str = Field(..., description="Dify API密钥")
    DIFY_API_BASE_URL: str = os.getenv("DIFY_API_BASE_URL", "https://api.dify.ai/v1")
    SECRET_KEY: str = Field(..., description="JWT密钥")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    PG_VECTOR_URL: str = os.getenv("PG_VECTOR_URL", "postgresql://postgres:password@localhost:5432/vector_db")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    EMBEDDING_DIM: int = int(os.getenv("EMBEDDING_DIM", "1536"))
    
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    
    ALLOWED_ORIGINS: list = os.getenv("ALLOWED_ORIGINS", "*").split(",")

settings = Settings(
    PROJECT_NAME=os.getenv("PROJECT_NAME", "留学机构智能助手平台"),
    DATABASE_URL=os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/ai_companion"),
    REDIS_URL=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    DIFY_API_KEY=os.getenv("DIFY_API_KEY", ""),
    SECRET_KEY=os.getenv("SECRET_KEY", "your-secret-key-here")
)