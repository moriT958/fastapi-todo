from sqlalchemy.orm import Session
from models import Todo
from typing import List, Optional
from schemas import TodoCreate, TodoUpdate


# READ
def get_all_todos(db: Session, user_id: int) -> List[Todo]:
    return db.query(Todo).filter(Todo.user_id==user_id).all()

def get_todo_by_id(db: Session, id: int, user_id: int) -> Optional[Todo]:
    return db.query(Todo).filter(Todo.id==id).filter(Todo.user_id==user_id).first()

# CREATE
def create_todo(db: Session, todo_create: TodoCreate, user_id: int) -> Todo:
    # すでに村座いる場合はNoneを返す
    existing_todo = db.query(Todo).filter(Todo.user_id == user_id, Todo.title == todo_create.title).first()
    if existing_todo:
        return None

    new_todo = Todo(
        **todo_create.model_dump(),
        user_id=user_id
    )
    db.add(new_todo)
    db.commit()
    return new_todo

# UPDATE
def update_todo(db: Session, id: int, todo_update: TodoUpdate, user_id: int) -> Optional[Todo]:
    updating_todo = get_todo_by_id(db, id, user_id)
    if updating_todo is None:
        return None
    # updating_todo.title = updating_todo.title if todo_update.title is None else todo_update.title
    updating_todo.status = updating_todo.status if todo_update.status is None else todo_update.status
    db.add(updating_todo)
    db.commit()
    return updating_todo


# DELETE
def delete_todo(db: Session, id: int, user_id: int) -> Optional[Todo]:
    deleting_todo = get_todo_by_id(db, id, user_id)
    if deleting_todo is None:
        return None
    db.delete(deleting_todo)
    db.commit()
    return deleting_todo