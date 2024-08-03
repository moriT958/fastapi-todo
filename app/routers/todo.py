from fastapi import APIRouter, Depends, status, Path, HTTPException
from typing import Annotated, List
from models import Todo
from sqlalchemy.orm import Session
from database import get_db
from cruds import todo as todo_cruds
from schemas import TodoResponse, TodoCreate, TodoUpdate


router = APIRouter(prefix="/todos", tags=["Todos"])

dbDep = Annotated[Session, Depends(get_db)]  # get_dbに依存したSession型を作成


# 全てのTodoを取得
@router.get('/', response_model=list[TodoResponse], status_code=status.HTTP_200_OK)
async def get_all_todos(db: dbDep) -> List[Todo]:
    return todo_cruds.get_all_todos(db)


# 指定したIDのTodoを取得
@router.get('/{id}', response_model=TodoResponse, status_code=status.HTTP_200_OK)
async def get_todo_by_id(db: dbDep, id: int=Path(gt=0)):
    todo = todo_cruds.get_todo_by_id(db, id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


# 新規のTodoを作成
@router.post('/', response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(db: dbDep, todo_create: TodoCreate):
    return todo_cruds.create_todo(db, todo_create)


# Todoの内容を変更
@router.patch('/{id}', response_model=TodoResponse, status_code=status.HTTP_200_OK) 
async def update_todo(db: dbDep, todo_update: TodoUpdate, id: int=Path(gt=0)):
    updating_todo = todo_cruds.update_todo(db, id, todo_update)
    if not updating_todo:
        raise HTTPException(status_code=404, detail="Todo not updated")
    return updating_todo


# Todoを削除
@router.delete('/{id}', response_model=TodoResponse, status_code=status.HTTP_200_OK)
async def delete_todo(db: dbDep, id: int=Path(gt=0)):
    deleting_todo = todo_cruds.delete_todo(db, id)
    if not deleting_todo:
        raise HTTPException(status_code=404, detail="Todo not deleted")
    return deleting_todo