from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """用戶基礎 Schema"""
    username: str
    email: EmailStr


class UserCreate(UserBase):
    """用戶註冊"""
    password: str


class UserLogin(BaseModel):
    """用戶登入"""
    username: str
    password: str


class UserResponse(UserBase):
    """用戶回應"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Token"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token 資料"""
    username: Optional[str] = None
