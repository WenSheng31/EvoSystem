from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional
from ..core.validators import PasswordValidator, UsernameValidator


class UserBase(BaseModel):
    username: str
    email: EmailStr
    bio: Optional[str] = None

    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        return UsernameValidator.validate(v)

    @field_validator('bio')
    @classmethod
    def validate_bio(cls, v):
        if v is not None and len(v) > 200:
            raise ValueError('個人簡介最多 200 個字符')
        return v


class UserCreate(UserBase):
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        return PasswordValidator.validate(v)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None
    password: Optional[str] = None
    old_password: Optional[str] = None

    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        if v is None:
            return v
        return UsernameValidator.validate(v)

    @field_validator('bio')
    @classmethod
    def validate_bio(cls, v):
        if v is not None and len(v) > 200:
            raise ValueError('個人簡介最多 200 個字符')
        return v

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if v is None:
            return v
        return PasswordValidator.validate(v)


class UserResponse(UserBase):
    id: int
    avatar: Optional[str] = None
    bio: Optional[str] = None
    role: str = "user"
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AdminPasswordReset(BaseModel):
    new_password: str

    @field_validator('new_password')
    @classmethod
    def validate_password(cls, v):
        return PasswordValidator.validate(v)
