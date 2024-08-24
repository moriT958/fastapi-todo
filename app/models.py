from database import Base
from schemas import TodoStatus
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship


class Todo(Base):
    __tablename__ = "todos"
    __table_args__ = (UniqueConstraint("user_id", "title", name="user_title_uc"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    status = Column(Enum(TodoStatus), nullable=False, default=TodoStatus.WAITING)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    user = relationship("User", back_populates="todos")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    todos = relationship("Todo", back_populates="user")
