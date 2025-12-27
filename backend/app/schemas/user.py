from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional
from ..core.validators import PasswordValidator, UsernameValidator


class UserBase(BaseModel):
    """用戶基礎 Schema"""
    username: str
    email: EmailStr
    bio: Optional[str] = None

    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        """驗證用戶名格式"""
        return UsernameValidator.validate(v)

    @field_validator('bio')
    @classmethod
    def validate_bio(cls, v):
        """驗證個人簡介長度"""
        if v is not None and len(v) > 200:
            raise ValueError('個人簡介最多 200 個字符')
        return v


class UserCreate(UserBase):
    """用戶註冊"""
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """驗證密碼強度"""
        return PasswordValidator.validate(v)


class UserLogin(BaseModel):
    """用戶登入"""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """用戶更新"""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None
    password: Optional[str] = None
    old_password: Optional[str] = None

    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        """驗證用戶名格式"""
        if v is None:
            return v
        return UsernameValidator.validate(v)

    @field_validator('bio')
    @classmethod
    def validate_bio(cls, v):
        """驗證個人簡介長度"""
        if v is not None and len(v) > 200:
            raise ValueError('個人簡介最多 200 個字符')
        return v

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """驗證密碼強度"""
        if v is None:
            return v
        return PasswordValidator.validate(v)


class UserResponse(UserBase):
    """用戶回應"""
    id: int
    avatar: Optional[str] = None
    bio: Optional[str] = None
    role: str = "user"
    is_active: bool = True
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


class AdminPasswordReset(BaseModel):
    """管理員重置用戶密碼"""
    new_password: str

    @field_validator('new_password')
    @classmethod
    def validate_password(cls, v):
        """驗證密碼強度"""
        return PasswordValidator.validate(v)
