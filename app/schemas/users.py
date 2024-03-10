from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, UUID4, Field, validator, field_validator

from app.models.users import Users


class UserCreate(BaseModel):
    """ Проверяет sign-up запрос """
    email: EmailStr
    password: str

class UserBase(BaseModel):
    """ Формирует тело ответа с деталями пользователя """
    id: int
    email: EmailStr


class UserAddress(BaseModel):
    region: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    num_of_house: Optional[str] = None
    postcode: Optional[int] = None



class UserUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    patronymic: Optional[str] = None
    address: Optional[UserAddress] = None



class TokenBase(BaseModel):
    token: UUID4 = Field(..., alias="access_token")
    expires: datetime
    token_type: Optional[str] = "bearer"

    class Config:
        populate_by_name = True

    @field_validator("token")
    def hexlify_token(cls, value):
        """ Конвертирует UUID в hex строку """
        return value.hex


class User(UserBase):
    """Формирует тело ответа с деталями пользователя и токеном"""
    token: TokenBase = {}
    role: str
    name: Optional[str] = None
    surname: Optional[str] = None
    patronymic: Optional[str] = None
    address: Optional[UserAddress] = None

    @classmethod
    def from_db_user(cls, db_user: Users, token_dict: TokenBase) -> "User":
        return cls(
            id=db_user.id,
            email=db_user.email,
            name=db_user.name,
            role=db_user.role,
            surname=db_user.surname,
            patronymic=db_user.patronymic,
            address=UserAddress(
                region=db_user.address.region,
                city=db_user.address.city,
                street=db_user.address.street,
                num_of_house=db_user.address.num_of_house,
                postcode=db_user.address.postcode
            ),
            is_active=True,
            token=token_dict
        )