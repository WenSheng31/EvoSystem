from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """應用配置"""
    # 資料庫
    DATABASE_URL: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # 應用
    PROJECT_NAME: str = "會員系統 API"
    API_V1_PREFIX: str = "/api"

    # CORS（只允許特定來源，提升安全性）
    # 開發環境：localhost 的不同端口
    # 生產環境：請在 .env 文件中覆蓋此設定為實際域名
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost:5173",  # Vite 開發服務器
        "http://localhost:3000",  # 備用端口
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    # 檔案上傳
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS: list = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
    UPLOAD_DIR: str = "uploads"

    class Config:
        env_file = ".env"


settings = Settings()
