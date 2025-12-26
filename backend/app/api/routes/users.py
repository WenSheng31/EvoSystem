from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
import os
import uuid
from pathlib import Path
from ...core.security import get_current_user, get_password_hash
from ...core.database import get_db
from ...core.config import settings
from ...models.user import User
from ...schemas.user import UserResponse, UserUpdate

router = APIRouter()

# 上傳目錄設定
UPLOAD_DIR = Path(__file__).parent.parent.parent.parent / settings.UPLOAD_DIR / "avatars"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_EXTENSIONS = set(settings.ALLOWED_EXTENSIONS)
MAX_FILE_SIZE = settings.MAX_FILE_SIZE


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """獲取當前用戶資訊"""
    return current_user


@router.patch("/me", response_model=UserResponse)
def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新當前用戶資訊"""
    # 檢查用戶名是否已被使用
    if user_update.username and user_update.username != current_user.username:
        existing_user = db.query(User).filter(User.username == user_update.username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用戶名已被使用"
            )
        current_user.username = user_update.username

    # 檢查郵箱是否已被使用
    if user_update.email and user_update.email != current_user.email:
        existing_user = db.query(User).filter(User.email == user_update.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="郵箱已被使用"
            )
        current_user.email = user_update.email

    # 更新個人簡介
    if user_update.bio is not None:
        current_user.bio = user_update.bio

    # 更新密碼
    if user_update.password:
        current_user.hashed_password = get_password_hash(user_update.password)

    db.commit()
    db.refresh(current_user)
    return current_user


@router.post("/avatar", response_model=UserResponse)
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """上傳用戶頭像"""
    # 檢查檔案類型
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"不支援的檔案格式。允許的格式：{', '.join(ALLOWED_EXTENSIONS)}"
        )

    # 讀取檔案內容並檢查大小
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="檔案大小超過 5MB 限制"
        )

    # 刪除舊頭像
    if current_user.avatar:
        # 從相對路徑轉換為絕對路徑
        if current_user.avatar.startswith("backend/"):
            old_filename = current_user.avatar.split("/")[-1]
            old_avatar_path = UPLOAD_DIR / old_filename
        else:
            old_avatar_path = Path(current_user.avatar)

        if old_avatar_path.exists():
            old_avatar_path.unlink()

    # 生成唯一檔名
    filename = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / filename

    # 儲存檔案
    with open(file_path, "wb") as f:
        f.write(contents)

    # 更新資料庫 - 儲存相對路徑
    relative_path = f"backend/uploads/avatars/{filename}"
    current_user.avatar = relative_path
    db.commit()
    db.refresh(current_user)

    return current_user
