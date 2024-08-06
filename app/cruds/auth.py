from config import get_settings
from schemas import UserCreate, DecodedToken
from models import User

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional
import base64
import os
import hashlib
from jose import jwt, JWTError
from datetime import timedelta, datetime


ALGORITHM = "HS256"
SECRET_KEY = get_settings().secret_key

# ログイン時に使用するFastAPIの認証フロー
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")

# 新ユーザの作成
def create_user(db: Session, user_create: UserCreate) -> User:

    # クライアントから受け取ったパスワードのハッシュ化
    salt = base64.b64encode(os.urandom(32))
    hashed_password = hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=user_create.password.encode(),
        salt=salt,
        iterations=1000
    ).hex()

    # 新ユーザの作成・追加
    new_user = User(
        username=user_create.username,
        password=hashed_password,
        salt=salt.decode()
    )
    db.add(new_user)
    db.commit()

    return new_user


# ユーザログイン

# ユーザの検証
def authenticate_user(db: Session, username: str, password: str) -> User:
    user = db.query(User).filter(User.username==username).first()
    if not user:
        return None
    
    hased_password = hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode(),
        salt=user.salt.encode(),
        iterations=1000
    ).hex()
    if user.password != hased_password:
        return None
    
    return user
    
# クライアントに返すアクセストークンの生成
def create_access_token(username: str, user_id: int, expire_delta: timedelta) -> str:
    expires_at = datetime.now() + expire_delta
    payload = {
        "sub": username,
        "id": user_id,
        "exp": expires_at
    }
    return jwt.encode(payload, SECRET_KEY, ALGORITHM)  # jwtを生成して返却

# ログイン中ユーザの取得
def get_current_user(access_token: str = Depends(oauth2_schema)) -> Optional[DecodedToken]:
    try:
        payload = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
        username = payload.get("sub")
        user_id = payload.get("id")

        if username is None or user_id is None:
            return None
        
        return DecodedToken(username=username, user_id=user_id)
    
    except JWTError:
        raise JWTError