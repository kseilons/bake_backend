from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from app.models.database import get_db
from app.schemas import users
from app.controllers import users as users_controller
from app.utils import users as users_utils
from app.utils.dependecies import get_current_user

router = APIRouter(tags=['users'])


@router.post("/sign-up", response_model=users.User)
async def create_user(user: users.UserCreate, db: Session = Depends(get_db)):
    db_user = await users_controller.get_user_by_email(email=user.email, db=db)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await users_controller.create_user(user=user, db=db)


@router.post("/auth", response_model=users.TokenBase)
async def auth(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await users_controller.get_user_by_email(email=form_data.username, db=db)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not users_utils.validate_password(
            password=form_data.password, hashed_password=user.hashed_password
    ):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    return await users_controller.create_user_token(user_id=user.id, db=db)

@router.post("/users/update", response_model=users.User)
async def update_user(user: users.UserUpdate,
                      db: Session = Depends(get_db),
                      current_user: users.User = Depends(get_current_user)
):
    return await users_controller.update_user(user, current_user, db)


@router.get("/users/me", response_model=users.User)
async def get_user(current_user: users.User = Depends(get_current_user)):
    return current_user


@router.delete("/users/{user_id}")
async def delete_user(
        user_id: int,
        current_user: users.User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    # Проверяем, является ли текущий пользователь владельцем удаляемого аккаунта
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this account"
        )

    await users_controller.delete_user(user_id, db)
    return {"message": "User deleted successfully"}