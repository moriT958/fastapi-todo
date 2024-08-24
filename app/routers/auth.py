from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from typing import Annotated
from sqlalchemy.orm import Session
from datetime import timedelta

from database import get_db
from models import User
from schemas import UserCreate, UserResponse, Token
from cruds import auth as auth_cruds


router = APIRouter(prefix="/auth", tags=["Auth"])

dbDep = Annotated[Session, Depends(get_db)]


@router.post(
    "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def create_user(db: dbDep, user_create: UserCreate):

    # ユーザ名の検証
    if db.query(User).filter(User.username == user_create.username).first():
        raise HTTPException(400, "already registered.")

    return auth_cruds.create_user(db, user_create)


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login_user(
    db: dbDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = auth_cruds.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401, detail="username or password is incorrect."
        )

    token = auth_cruds.create_access_token(
        user.username, user.id, timedelta(minutes=15)
    )
    return {"access_token": token, "token_type": "bearer"}
