from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional


class TodoBase(BaseModel):
    """待辦事項基礎 Schema"""
    title: str

    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        """驗證待辦事項標題"""
        if not v or not v.strip():
            raise ValueError('待辦事項標題不能為空')
        if len(v) > 200:
            raise ValueError('待辦事項標題最多 200 個字符')
        return v.strip()


class TodoCreate(TodoBase):
    """建立待辦事項"""
    pass


class TodoUpdate(BaseModel):
    """更新待辦事項"""
    title: Optional[str] = None
    is_completed: Optional[bool] = None

    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        """驗證待辦事項標題"""
        if v is not None:
            if not v.strip():
                raise ValueError('待辦事項標題不能為空')
            if len(v) > 200:
                raise ValueError('待辦事項標題最多 200 個字符')
            return v.strip()
        return v


class TodoResponse(TodoBase):
    """待辦事項回應"""
    id: int
    user_id: int
    is_completed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
