from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .core.config import settings
from .core.database import engine, Base
from .api.routes import auth, users, admin
from pathlib import Path

# 導入所有模型（確保 SQLAlchemy 知道這些模型）
from .models.user import User

# 創建資料庫表
Base.metadata.create_all(bind=engine)

# 建立應用
app = FastAPI(title=settings.PROJECT_NAME)

# 靜態文件服務
UPLOAD_DIR = Path(__file__).parent.parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# 註冊路由
app.include_router(auth.router, prefix=settings.API_V1_PREFIX, tags=["認證"])
app.include_router(users.router, prefix=settings.API_V1_PREFIX, tags=["用戶"])
app.include_router(admin.router, prefix=f"{settings.API_V1_PREFIX}/admin", tags=["管理員"])


@app.get("/")
def read_root():
    return {"message": settings.PROJECT_NAME}
