from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.database import engine, Base
from .api.routes import auth, users

# 創建資料庫表
Base.metadata.create_all(bind=engine)

# 建立應用
app = FastAPI(title=settings.PROJECT_NAME)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 註冊路由
app.include_router(auth.router, prefix=settings.API_V1_PREFIX, tags=["認證"])
app.include_router(users.router, prefix=settings.API_V1_PREFIX, tags=["用戶"])


@app.get("/")
def read_root():
    return {"message": settings.PROJECT_NAME}
