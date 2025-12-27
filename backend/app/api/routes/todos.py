from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...core.security import get_current_user
from ...core.database import get_db
from ...models.user import User
from ...models.todo import Todo
from ...schemas.todo import TodoCreate, TodoUpdate, TodoResponse

router = APIRouter()


@router.get("/todos", response_model=List[TodoResponse])
def get_todos(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """獲取當前用戶的所有待辦事項"""
    todos = db.query(Todo).filter(
        Todo.user_id == current_user.id
    ).order_by(Todo.created_at.desc()).all()
    return todos


@router.post("/todos", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo: TodoCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """建立新的待辦事項"""
    db_todo = Todo(title=todo.title, user_id=current_user.id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@router.patch("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新待辦事項"""
    db_todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == current_user.id
    ).first()

    if not db_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="待辦事項不存在")

    if todo_update.title is not None:
        db_todo.title = todo_update.title
    if todo_update.is_completed is not None:
        db_todo.is_completed = todo_update.is_completed

    db.commit()
    db.refresh(db_todo)
    return db_todo


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """刪除待辦事項"""
    db_todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == current_user.id
    ).first()

    if not db_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="待辦事項不存在")

    db.delete(db_todo)
    db.commit()
    return None
