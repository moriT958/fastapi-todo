from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from datetime import timedelta

from typing import Annotated
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserResponse, UserCreateForm, Token
from cruds import auth as auth_cruds

router = APIRouter(prefix="/auth", tags=["auth"])

DbDependency = Annotated[Session, Depends(get_db)]
FormDependency = Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)]


@router.post('/signup', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(db: DbDependency, user_create: UserCreateForm):
    return auth_cruds.create_user(db, user_create)


@router.post('/login', response_model=Token, status_code=status.HTTP_200_OK)
async def login(db: DbDependency, user_form: FormDependency):
    user = auth_cruds.authenticate_user(db, user_form.username, user_form.password)
    if not user:
        raise HTTPException(status_code=401, detail="username or password incorrect")
    
    token = auth_cruds.create_access_token(username=user.username, user_id=user.id, expires_delta=timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}