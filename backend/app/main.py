from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pathlib import Path

from .core.config import settings
from .core.database import engine, Base
from .api.routes import auth, users, admin
from .models.user import User
from .models.audit_log import AuditLog

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="EvoSystem API",
    version="2.0.0"
)

# 靜態文件服務（用於頭像等上傳檔案）
# 將上傳目錄掛載到 /api/uploads，以便與前端的 API_BASE_URL (/api) 對齊
# 這樣前端拼接 URL 時：/api + /uploads/xxx 就會正確指向這裡
UPLOAD_DIR = Path(__file__).parent.parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount(f"{settings.API_V1_PREFIX}/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# ==================== 安全 Headers 中介軟體 ====================
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    添加安全相關的 HTTP Headers
    保護網站免受 XSS、點擊劫持等攻擊
    """
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # 防止瀏覽器猜測檔案類型 (MIME sniffing)
        response.headers["X-Content-Type-Options"] = "nosniff"

        # 禁止被嵌入 iframe，防止點擊劫持 (Clickjacking)
        response.headers["X-Frame-Options"] = "DENY"

        # 開啟 XSS 防護過濾器 (針對舊版瀏覽器)
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # 限制 Referrer 資訊的傳送，保護隱私
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # 禁用不需要的瀏覽器功能 (如地理位置、麥克風)
        response.headers["Permissions-Policy"] = (
            "geolocation=(), "
            "microphone=(), "
            "camera=()"
        )

        return response


# ==================== CORS 配置 ====================
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,  # 設定允許的前端網域
    allow_credentials=True,                        # 允許跨域請求攜帶 Cookie (JWT 需要)
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

app.add_middleware(SecurityHeadersMiddleware)

app.include_router(auth.router, prefix=settings.API_V1_PREFIX, tags=["認證"])
app.include_router(users.router, prefix=settings.API_V1_PREFIX, tags=["用戶"])
app.include_router(admin.router, prefix=f"{settings.API_V1_PREFIX}/admin", tags=["管理員"])


@app.get("/")
def read_root():
    return {
        "message": f"歡迎使用 {settings.PROJECT_NAME}",
        "version": "2.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
