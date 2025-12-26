from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional
import re


class UserBase(BaseModel):
    """用戶基礎 Schema"""
    username: str
    email: EmailStr

    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        """驗證用戶名格式"""
        if len(v) < 3 or len(v) > 20:
            raise ValueError('用戶名長度必須在 3-20 個字符之間')
        if not re.match(r'^[a-zA-Z0-9_\u4e00-\u9fa5]+$', v):
            raise ValueError('用戶名只能包含字母、數字、下劃線和中文')
        return v


class UserCreate(UserBase):
    """用戶註冊"""
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """驗證密碼強度"""
        if len(v) < 8:
            raise ValueError('密碼至少需要 8 個字符')
        if len(v) > 50:
            raise ValueError('密碼最多 50 個字符')
        if not re.search(r'[A-Za-z]', v):
            raise ValueError('密碼必須包含至少一個字母')
        if not re.search(r'\d', v):
            raise ValueError('密碼必須包含至少一個數字')
        return v


class UserLogin(BaseModel):
    """用戶登入"""
    username: str
    password: str


class UserUpdate(BaseModel):
    """用戶更新"""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        """驗證用戶名格式"""
        if v is None:
            return v
        if len(v) < 3 or len(v) > 20:
            raise ValueError('用戶名長度必須在 3-20 個字符之間')
        if not re.match(r'^[a-zA-Z0-9_\u4e00-\u9fa5]+$', v):
            raise ValueError('用戶名只能包含字母、數字、下劃線和中文')
        return v

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """驗證密碼強度"""
        if v is None:
            return v
        if len(v) < 8:
            raise ValueError('密碼至少需要 8 個字符')
        if len(v) > 50:
            raise ValueError('密碼最多 50 個字符')
        if not re.search(r'[A-Za-z]', v):
            raise ValueError('密碼必須包含至少一個字母')
        if not re.search(r'\d', v):
            raise ValueError('密碼必須包含至少一個數字')
        return v


class UserResponse(UserBase):
    """用戶回應"""
    id: int
    avatar: Optional[str] = None
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
