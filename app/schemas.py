from pydantic import BaseModel, ConfigDict, Field
from enum import Enum
from datetime import datetime
from typing import Optional


class TodoStatus(Enum):
    WAITING = "WAITING"
    ON_PROC = "ON_PROC"
    COMPLETED = "COMPLETED"

class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=20, examples=["部屋の片付け"])

class TodoUpdate(BaseModel): 
    # 更新できるのはステータスのみに変更
    # title: Optional[str] = Field(None, min_length=1, max_length=20, examples=["部屋の片付け"])
    status: Optional[TodoStatus] = Field(None, examples=[TodoStatus.ON_PROC])

class TodoResponse(BaseModel):
    id: int = Field(gt=0, examples=[1])
    title: str = Field(min_length=1, max_length=20, examples=["部屋の片付け"])
    status: TodoStatus = Field(examples=[TodoStatus.ON_PROC])
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# 認証で使うスキーマ型
# 新規ユーザを作成するときのリクエストボディの型
class UserCreate(BaseModel):
    username: str = Field(min_length=1, examples=["user1"])
    password: str = Field(min_length=8, examples=["password"])


# サーバが返すユーザレスポンスの型
class UserResponse(BaseModel):
    id: int = Field(gt=0, examples=[1])
    username: str = Field(min_length=1, examples=["user1"])
    created_at: datetime
    updated_at: datetime

    # python側でこのスキーマに対応するインスタンスを作成する際、インスタンス化に用いた
    # クラスが持つ属性からインスタンスに与えることができる。
    # 通常のpydanticは辞書やkwargsからしか与えることができない。
    model_config = ConfigDict(from_attributes=True)


# アクセストークンの型
class Token(BaseModel):
    access_token: str
    token_type: str


# 複合後のアクセストークンから得たユーザ情報
class DecodedToken(BaseModel):
    username: str
    user_id: int