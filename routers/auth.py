from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

DbDependency = Annotated[Session, Depends(get_db)]
FormDependency = Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)]


# @router.post('/signup', )