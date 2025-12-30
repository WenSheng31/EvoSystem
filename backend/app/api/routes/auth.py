from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import timedelta
from slowapi import Limiter
from slowapi.util import get_remote_address

from ...core.database import get_db
from ...core.security import get_password_hash, verify_password, create_access_token, get_current_user
from ...core.config import settings
from ...models.user import User
from ...models.audit_log import AuditLog
from ...schemas.user import UserCreate, UserLogin, UserResponse

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


def create_audit_log(
    db: Session,
    user_id: int | None,
    action: str,
    request: Request,
    details: str | None = None
):
    audit_log = AuditLog(
        user_id=user_id,
        action=action,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        details=details
    )
    db.add(audit_log)
    db.commit()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def register(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    existing_username = db.query(User).filter(User.username == user.username).first()
    existing_email = db.query(User).filter(User.email == user.email).first()

    if existing_username or existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用戶名或郵箱已被使用"
        )

    hashed_password = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(new_user)

    try:
        db.commit()
        db.refresh(new_user)

        create_audit_log(
            db=db,
            user_id=new_user.id,
            action="register",
            request=request,
            details=f"用戶 {new_user.username} 註冊成功"
        )

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用戶名或郵箱已被使用"
        )

    return new_user


@router.post("/login", response_model=UserResponse)
@limiter.limit("5/minute")
def login(request: Request, credentials: UserLogin, response: Response, db: Session = Depends(get_db)):
    """
    用戶登入路由
    """
    # 根據 Email 查找用戶
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or not verify_password(credentials.password, user.hashed_password):
        create_audit_log(
            db=db,
            user_id=user.id if user else None,
            action="login_failed",
            request=request,
            details=f"郵箱：{credentials.email}"
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="郵箱或密碼錯誤",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="帳號已被停用，請聯繫管理員"
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role},
        expires_delta=access_token_expires
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/"
    )

    create_audit_log(
        db=db,
        user_id=user.id,
        action="login_success",
        request=request,
        details=f"用戶 {user.username} 登入成功"
    )

    return user


@router.post("/logout")
def logout(
    response: Response,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    create_audit_log(
        db=db,
        user_id=current_user.id,
        action="logout",
        request=request,
        details=f"用戶 {current_user.username} 登出"
    )

    response.delete_cookie(key="access_token", path="/")

    return {"message": "已成功登出"}
