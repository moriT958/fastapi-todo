from pydantic import BaseModel, ConfigDict, Field
from enum import Enum
from datetime import datetime


class TodoStatus(Enum):
    WAITING = "WAITING"
    COMPLETED = "COMPLETED"


# 認証で使うスキーマ型
# 新規ユーザを作成するときのリクエストボディの型
class UserCreateForm(BaseModel):
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


# サーバが返すアクセストークンの型
class Token(BaseModel):
    access_token: str
    token_type: str