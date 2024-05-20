from re import template
import uuid
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from app.models.database import get_db
from app.schemas import users as users_schemas

from app.controller import users as users_controller
from app.utils.dependecies import get_current_user
from app.utils.email.smtp_server import EmailSender

router = APIRouter(tags=['users'])

email_sender = EmailSender()

@router.post("/sign-up", response_model=users_schemas.UserCreateResponse)
async def create_user(user: users_schemas.UserCreate, db: Session = Depends(get_db)):
    return await users_controller.create_user(user, db)


@router.get("/confirm/{token}", response_model=users_schemas.TokenBase)
async def confirm_email(token: str, db: Session = Depends(get_db)):
    return await users_controller.confirm_email(token, db)

@router.post("/auth", response_model=users_schemas.TokenBase)
async def auth(auth_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return await users_controller.auth(auth_data, db)

@router.put("/users/update", response_model=users_schemas.User)
async def update_user(user: users_schemas.UserUpdate,
                    db: Session = Depends(get_db),
                    current_user: users_schemas.User = Depends(get_current_user)
):
    return await users_controller.update_user(user, current_user.id, db)


@router.get("/users/me", response_model=users_schemas.User)
async def get_user(current_user: users_schemas.User = Depends(get_current_user)):
    return current_user


@router.delete("/users/{user_id}")
async def delete_user(
        current_user: users_schemas.User = Depends(get_current_user),
        db: Session = Depends(get_db)
):

    await users_controller.delete_user(current_user.id, db)
    return {"message": "User deleted successfully"}



