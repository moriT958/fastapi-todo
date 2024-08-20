from fastapi import APIRouter, Depends, status, Path, HTTPException
from typing import Annotated, List
from models import Todo
from sqlalchemy.orm import Session
from database import get_db
from cruds import todo as todo_cruds, auth as auth_cruds
from schemas import TodoResponse, TodoCreate, TodoUpdate, DecodedToken


router = APIRouter(prefix="/todos", tags=["Todos"])

dbDep = Annotated[Session, Depends(get_db)]  # get_dbに依存したSession型を作成
userDep = Annotated[DecodedToken, Depends(auth_cruds.get_current_user)]


# 全てのTodoを取得
@router.get('/', response_model=list[TodoResponse], status_code=status.HTTP_200_OK)
async def get_all_todos(db: dbDep, user: userDep) -> List[Todo]:
    return todo_cruds.get_all_todos(db, user.user_id)


# 指定したIDのTodoを取得
@router.get('/{id}', response_model=TodoResponse, status_code=status.HTTP_200_OK)
async def get_todo_by_id(db: dbDep, user: userDep, id: int=Path(gt=0)):
    todo = todo_cruds.get_todo_by_id(db, id, user.user_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


# 新規のTodoを作成
@router.post('/', response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(db: dbDep, todo_create: TodoCreate, user: userDep):
    created_todo = todo_cruds.create_todo(db, todo_create, user.user_id)
    if not created_todo:
        raise HTTPException(status_code=400, detail="This Todo is already exits")
    return created_todo


# Todoの内容を変更
@router.patch('/{id}', response_model=TodoResponse, status_code=status.HTTP_200_OK) 
async def update_todo(db: dbDep, todo_update: TodoUpdate, user: userDep, id: int=Path(gt=0)):
    updating_todo = todo_cruds.update_todo(db, id, todo_update, user.user_id)
    if not updating_todo:
        raise HTTPException(status_code=404, detail="Todo not updated")
    return updating_todo


# Todoを削除
@router.delete('/{id}', response_model=TodoResponse, status_code=status.HTTP_200_OK)
async def delete_todo(db: dbDep, user: userDep, id: int=Path(gt=0)):
    deleting_todo = todo_cruds.delete_todo(db, id, user.user_id)
    if not deleting_todo:
        raise HTTPException(status_code=404, detail="Todo not deleted")
    return deleting_todo