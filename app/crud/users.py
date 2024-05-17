import uuid
from datetime import datetime, timedelta
from typing import Type

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.models.users import Users, Token, UsersAddress
from app.schemas import users as user_schema
from app.schemas.users import TokenBase, User
from app.utils.users import get_random_string, hash_password


async def get_user_by_email(email: str, db: Session):
    """ Возвращает информацию о пользователе """
    return db.query(Users).filter_by(email=email).first()


async def get_user_by_token(token: str, db: Session):
    """ Возвращает информацию о владельце указанного токена """
    return db.query(Token).filter_by(access_token=token).first().user

async def get_user_by_id(id: int, db: Session):
    """ Возвращает информацию о владельце указанного id """
    return db.query(Users).filter_by(id=id).first()

async def create_user_token(user_id: int, db: Session) -> user_schema.TokenBase:
    """ Создает токен для пользователя с указанным user_id """
    token = uuid.uuid4().hex
    # Устанавливаем срок действия токена (например, 1 день)
    expires_at = datetime.now() + timedelta(weeks=2)
    token = Token(access_token=token, expires=expires_at, user_id=user_id)
    db.add(token)
    db.commit()
    db.refresh(token)
    return token


async def create_user(user: user_schema.UserCreate, db: Session):
    """ Создает нового пользователя в БД """
    salt = get_random_string()
    hashed_password = hash_password(user.password, salt)
    db_user = Users(email=user.email, hashed_password=f"{salt}${hashed_password}")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def update_user(user_update: user_schema.UserUpdate, db_user: Users, db: Session):
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
    
async def save_verification_token(user_id: int, token: str, db: Session):
    user = db.query(Users).filter(Users.id == user_id).first()
    user.confirmation_token = token
    db.commit()
    db.refresh(user)
    
    
async def get_user_by_conf_token(token: str, db: Session):
    return db.query(Users).filter(Users.confirmation_token == token).first()


    
    
async def verify_user(user: Users, db: Session):
    user.is_verified = True
    user.confirmation_token = None  # Удаление токена после подтверждения
    db.commit()
    db.refresh(user)