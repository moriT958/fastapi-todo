from config import get_settings
from schemas import UserCreateForm
from models import User
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

import os
import base64
import hashlib
from datetime import timedelta, datetime
from jose import jwt, JWTError
from typing import Annotated


ALGORITHM = "HS256"  # JWT生成に用いるアルゴリズム
SECRET_KEY = get_settings().secret_key

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")


# 新規ユーザの作成
def create_user(db: Session, user_create: UserCreateForm):
    # ソルトの生成: 32バイトの乱数(バイナリ)を生成し、base64形式にエンコード
    salt = base64.b64encode(os.urandom(32))
    
    # パスワードのハッシュ化
    hashed_password = hashlib.pbkdf2_hmac(
        hash_name="sha256",  # 使用するハッシュ関数の名前
        password=user_create.password.encode(),
        salt=salt,
        iterations=1000 
    ).hex()  # 見やすくするため16進数に変換

    new_user = User(
        username=user_create.username,
        password=hashed_password,
        salt=salt.decode()
    )
    db.add(new_user)
    db.commit()

    return new_user


# ユーザが登録されているかどうかの確認
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username==username).first()
    if not user:
        return None

    hashed_password = hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode(),
        salt=user.salt.encode(),
        iterations=1000
    ).hex()
    if user.password != hashed_password:
        return None
    
    return user


# ユーザに対してアクセストークンを作成する
def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    expires_at = datetime.now() + expires_delta  # 有効期限
    payload = {"sub": username, "id": user_id, "exp": expires_at}  # トークンの本体部分
    return jwt.encode(claims=payload, key=SECRET_KEY, algorithm=ALGORITHM)


