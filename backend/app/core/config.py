from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    COOKIE_SECURE: bool = False
    BACKEND_CORS_ORIGINS: list = ["http://localhost:5173"]

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    PROJECT_NAME: str = "會員系統 API"
    API_V1_PREFIX: str = "/api"
    MAX_FILE_SIZE: int = 5 * 1024 * 1024
    ALLOWED_EXTENSIONS: list = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
    UPLOAD_DIR: str = "uploads"

    class Config:
        env_file = ".env"


settings = Settings()
