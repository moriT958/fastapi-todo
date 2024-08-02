from fastapi import APIRouter, Depends, status, Path, HTTPException
from typing import Annotated, List
from models import Todo
from sqlalchemy.orm import Session
from database import get_db
from cruds import todo as todo_cruds
from schemas import TodoResponse, TodoCreate


router = APIRouter(prefix="/todos", tags=["Todos"])

dbDep = Annotated[Session, Depends(get_db)]  # get_dbに依存したSession型を作成


@router.get('/', response_model=list[TodoResponse], status_code=status.HTTP_200_OK)
async def get_all_todos(db: dbDep) -> List[Todo]:
    return todo_cruds.get_all_todos(db)


@router.get('/{id}', response_model=TodoResponse, status_code=status.HTTP_200_OK)
async def get_todo_by_id(db: dbDep, id: int=Path(gt=0)):
    todo = todo_cruds.get_todo_by_id(db, id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.post('/', response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(db: dbDep, todo_create: TodoCreate):
    return todo_cruds.create_todo(db, todo_create)