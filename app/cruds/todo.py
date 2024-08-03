from sqlalchemy.orm import Session
from models import Todo
from typing import List, Optional
from schemas import TodoCreate, TodoUpdate


# READ
def get_all_todos(db: Session) -> List[Todo]:
    return db.query(Todo).all()

def get_todo_by_id(db: Session, id: int) -> Optional[Todo]:
    return db.query(Todo).filter(Todo.id==id).first()

# CREATE
def create_todo(db: Session, todo_create: TodoCreate) -> Todo:
    new_todo = Todo(
        **todo_create.model_dump()
    )
    db.add(new_todo)
    db.commit()
    return new_todo

# UPDATE
def update_todo(db: Session, id: int, todo_update: TodoUpdate) -> Optional[Todo]:
    updating_todo = get_todo_by_id(db, id)
    if updating_todo is None:
        return None
    # updating_todo.title = updating_todo.title if todo_update.title is None else todo_update.title
    updating_todo.status = updating_todo.status if todo_update.status is None else todo_update.status
    db.add(updating_todo)
    db.commit()
    return updating_todo


# DELETE
def delete_todo(db: Session, id: int) -> Optional[Todo]:
    deleting_todo = get_todo_by_id(db, id)
    if deleting_todo is None:
        return None
    db.delete(deleting_todo)
    db.commit()
    return deleting_todo