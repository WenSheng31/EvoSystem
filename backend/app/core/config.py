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

    # CORS（開發環境允許所有來源，生產環境需要設定具體網址）
    BACKEND_CORS_ORIGINS: list = ["*"]

    # 檔案上傳
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS: list = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
    UPLOAD_DIR: str = "uploads"

    class Config:
        env_file = ".env"


settings = Settings()
