from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from pathlib import Path
import math

from ...core.database import get_db
from ...core.security import get_admin_user, get_password_hash
from ...core.config import settings
from ...core.file_utils import AvatarManager
from ...models.user import User
from ...models.audit_log import AuditLog
from ...schemas.user import UserResponse, AdminPasswordReset
from ...schemas.audit_log import AuditLogResponse, AuditLogListResponse

router = APIRouter()

UPLOAD_DIR = Path(__file__).parent.parent.parent.parent / settings.UPLOAD_DIR / "avatars"


@router.get("/users", response_model=List[UserResponse])
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
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
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用戶不存在"
        )

    if user.id == admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能停用自己的帳號"
        )

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
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用戶不存在"
        )

    if user.id == admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能刪除自己的帳號"
        )

    if user.avatar:
        AvatarManager.delete_avatar(user.avatar, UPLOAD_DIR)

    db.delete(user)
    db.commit()

    return {"message": f"用戶 {user.username} 已被刪除"}


@router.patch("/users/{user_id}/reset-password")
def reset_user_password(
    user_id: int,
    password_data: AdminPasswordReset,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用戶不存在"
        )

    if user.id == admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能重置自己的密碼，請使用正常的修改密碼流程"
        )

    user.hashed_password = get_password_hash(password_data.new_password)
    db.commit()

    return {"message": f"用戶 {user.username} 的密碼已重置"}


@router.get("/audit-logs", response_model=AuditLogListResponse)
def get_audit_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    action: Optional[str] = Query(None),
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    query = db.query(
        AuditLog.id,
        AuditLog.user_id,
        User.username,
        AuditLog.action,
        AuditLog.ip_address,
        AuditLog.user_agent,
        AuditLog.details,
        AuditLog.created_at
    ).outerjoin(User, AuditLog.user_id == User.id)

    if action:
        query = query.filter(AuditLog.action == action)

    query = query.order_by(AuditLog.created_at.desc())

    offset = (page - 1) * page_size
    results = query.offset(offset).limit(page_size + 1).all()

    has_more = len(results) > page_size
    if has_more:
        results = results[:page_size]

    total = page * page_size if has_more else offset + len(results)
    total_pages = page + 1 if has_more else page

    logs = [
        AuditLogResponse(
            id=row[0],
            user_id=row[1],
            username=row[2],
            action=row[3],
            ip_address=row[4],
            user_agent=row[5],
            details=row[6],
            created_at=row[7]
        )
        for row in results
    ]

    db.expunge_all()

    return AuditLogListResponse(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        logs=logs
    )
