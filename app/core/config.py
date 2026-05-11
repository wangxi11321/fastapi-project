import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class Settings(BaseModel):
    PROJECT_NAME: str = "留学机构智能助手平台"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/ai_companion")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    DIFY_API_KEY: str = os.getenv("DIFY_API_KEY", "")
    DIFY_API_BASE_URL: str = os.getenv("DIFY_API_BASE_URL", "https://api.dify.ai/v1")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

settings = Settings()