import uuid
from datetime import datetime, timedelta
from typing import Type

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.models.users import Users, Token, UsersAddress
from app.schemas import users as user_schema
from app.schemas.users import TokenBase, User
from app.utils.users import get_random_string, hash_password, is_admin


async def get_user_by_email(email: str, db: Session):
    """ Возвращает информацию о пользователе """
    return db.query(Users).filter_by(email=email).first()


async def get_user_by_token(token: str, db: Session):
    """ Возвращает информацию о владельце указанного токена """
    return db.query(Token).filter_by(token=token).first().user

async def create_user_token(user_id: int, db: Session):
    """ Создает токен для пользователя с указанным user_id """
    token = uuid.uuid4().hex
    # Устанавливаем срок действия токена (например, 1 день)
    expires_at = datetime.now() + timedelta(weeks=2)
    token = Token(token=token, expires=expires_at, user_id=user_id)
    db.add(token)
    db.commit()
    db.refresh(token)
    return token


async def create_user(user: user_schema.UserCreate, db: Session):
    """ Создает нового пользователя в БД """
    salt = get_random_string()
    hashed_password = hash_password(user.password, salt)
    role = 'user'
    if is_admin(user.email):
        role = 'admin'
    db_user = Users(email=user.email, hashed_password=f"{salt}${hashed_password}", role=role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    user_id = db_user.id
    token = await create_user_token(user_id, db)
    token_dict = TokenBase(token=token.token, expires=token.expires)
    return user_schema.User.from_db_user(db_user, token_dict)


async def update_user(user_update: user_schema.UserUpdate, current_user: user_schema.User, db: Session):
    db_user = db.query(Users).filter_by(id=current_user.id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Обновляем свойства пользователя
    for field, value in user_update.dict().items():
        if field != 'address':
            setattr(db_user, field, value)

    # Обновляем адрес пользователя, если он указан в обновлении
    if user_update.address:
        if db_user.address:
            # Если у пользователя уже есть адрес, обновляем его
            for field, value in user_update.address.dict().items():
                setattr(db_user.address, field, value)
        else:
            # Если у пользователя еще нет адреса, создаем новую запись адреса
            new_address = UsersAddress(**user_update.address.dict(), user_id=db_user.id)
            db.add(new_address)

    db.commit()
    db.refresh(db_user)
    return db_user

async def delete_user(user_id: int, db: Session) -> None:
    db_user = db.query(Users).filter_by(id=user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(db_user)
    db.commit()