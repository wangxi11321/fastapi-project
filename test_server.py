from fastapi import FastAPI
import uvicorn

app = FastAPI(title="AI中台测试服务", version="1.0.0")

@app.get("/")
async def root():
    return {
        "message": "AI中台架构升级完成",
        "version": "2.0.0",
        "status": "running"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/docs")
async def docs():
    return {"message": "API文档页面"}

if __name__ == "__main__":
    print("=" * 60)
    print("留学机构智能助手平台 - AI中台架构")
    print("=" * 60)
    print("📱 API文档: http://127.0.0.1:8000/docs")
    print("🏥 健康检查: http://127.0.0.1:8000/health")
    print("=" * 60)
    uvicorn.run("test_server:app", host="127.0.0.1", port=8000, reload=True)
