from re import template
import uuid
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from app.auth.auth import fastapi_users

from app.auth.schemas import IUser, IUserUpdate

router = APIRouter(tags=['users'], prefix='/users')

router.include_router(
    fastapi_users.get_users_router(IUser, IUserUpdate)
)


