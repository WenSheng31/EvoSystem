from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from ...core.database import get_db
from ...core.security import get_password_hash, verify_password, create_access_token
from ...core.config import settings
from ...models.user import User
from ...schemas.user import UserCreate, UserLogin, UserResponse, Token

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """用戶註冊"""
    # 檢查用戶名
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用戶名已被使用"
        )

    # 檢查郵箱
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="郵箱已被使用"
        )

    # 創建用戶
    hashed_password = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """用戶登入"""
    user = db.query(User).filter(User.username == credentials.username).first()

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用戶名或密碼錯誤",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
