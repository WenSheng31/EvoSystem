from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pathlib import Path

from ...core.database import get_db
from ...core.security import get_admin_user
from ...core.config import settings
from ...models.user import User
from ...schemas.user import UserResponse

router = APIRouter()

# 上傳目錄設定
UPLOAD_DIR = Path(__file__).parent.parent.parent.parent / settings.UPLOAD_DIR / "avatars"


@router.get("/users", response_model=List[UserResponse])
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """獲取所有用戶列表（僅管理員）"""
    # 驗證參數範圍
    if skip < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="skip 參數不能為負數"
        )
    if limit < 1 or limit > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="limit 參數必須在 1 到 1000 之間"
        )

    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.patch("/users/{user_id}/toggle-active", response_model=UserResponse)
def toggle_user_active(
    user_id: int,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """啟用/停用用戶（僅管理員）"""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用戶不存在"
        )

    # 不能停用自己
    if user.id == admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能停用自己的帳號"
        )

    # 切換啟用狀態
    user.is_active = not user.is_active
    db.commit()
    db.refresh(user)

    return user


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """刪除用戶（僅管理員）"""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用戶不存在"
        )

    # 不能刪除自己
    if user.id == admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能刪除自己的帳號"
        )

    # 刪除用戶頭像文件
    if user.avatar:
        try:
            if user.avatar.startswith("backend/uploads/avatars/"):
                filename = user.avatar.split("/")[-1]
                if ".." not in filename and "/" not in filename and "\\" not in filename:
                    avatar_path = UPLOAD_DIR / filename
                    if avatar_path.resolve().parent == UPLOAD_DIR.resolve():
                        if avatar_path.exists() and avatar_path.is_file():
                            avatar_path.unlink()
        except (ValueError, OSError):
            # 忽略刪除錯誤，繼續刪除用戶
            pass

    # 刪除用戶
    db.delete(user)
    db.commit()

    return {"message": f"用戶 {user.username} 已被刪除"}
