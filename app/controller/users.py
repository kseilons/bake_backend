from re import template
import uuid
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from app.models.database import get_db
from app.schemas import users as users_schemas
from app.crud import users as users_crud
from app.utils import users as users_utils
from app.utils.dependecies import get_current_user
from app.utils.email.smtp_server import email_sender
from app.utils.email.template_renderer import render_template
from app.setting import confirm_email_url



async def create_user(user: users_schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = await users_crud.get_user_by_email(email=user.email, db=db)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Создание нового пользователя с непроверенным статусом
    new_user = await users_crud.create_user(user=user, db=db)

    # Генерация уникального токена
    token = str(uuid.uuid4())
    
    # Сохранение токена в БД 
    await users_crud.save_verification_token(user_id=new_user.id, token=token, db=db)
    
    confirmation_link = confirm_email_url + token
    html_content = render_template('email_confirm.html', {'confirmation_link': confirmation_link})
    # Отправка письма с подтверждением
    await email_sender.send_email(
        email_to=user.email,
        subject='Подтвердите свою почту',
        body=html_content
    )
    return new_user

async def confirm_email(token: str, db: Session = Depends(get_db)) -> users_schemas.TokenBase:
    # Найти пользователя по токену
    user = await users_crud.get_user_by_conf_token(token=token, db=db)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid confirmation token")

    # Обновить статус пользователя на проверенный
    await users_crud.verify_user(user=user, db=db)
    response = await users_crud.create_user_token(user.id, db)
    response.role = user.role
    return response


async def auth(auth_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> users_schemas.TokenBase:
    user = await users_crud.get_user_by_email(email=auth_data.username, db=db)

    if not user:
        raise HTTPException(status_code=404, detail="Неправильный email")

    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Вы не подтвердили почту")
    
    if not users_utils.validate_password(
            password=auth_data.password, hashed_password=user.hashed_password
    ):
        raise HTTPException(status_code=401, detail="Неправильный email или пароль")

    response = await users_crud.create_user_token(user.id, db)
    response.role = user.role
    return response




async def update_user(user_update: users_schemas.UserUpdate, user_id: int,  db: Session):
    user = await users_crud.get_user_by_id(user_id, db)
    return await users_crud.update_user(user_update, user, db)


async def delete_user(user_id: int, db: Session) -> None:

    return await users_crud.delete_user(user_id, db)

