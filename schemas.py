from pydantic import BaseModel
from enum import Enum


class TodoStatus(Enum):
    WAITING = "WAITING"
    COMPLETED = "COMPLETED"