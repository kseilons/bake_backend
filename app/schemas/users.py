from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, UUID4, Field, validator, field_validator

from app.models.users import Users


class UserCreate(BaseModel):
    """ Проверяет sign-up запрос """
    email: EmailStr
    password: str

class UserCreateResponse(BaseModel):
    role: Optional[str] = None
    email: Optional[EmailStr] = None
    is_verified: Optional[bool] = None
    class Config:
        from_attributes = True


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
    access_token: UUID4 = Field(..., alias="access_token")
    expires: datetime
    token_type: Optional[str] = "bearer"
    role: Optional[str] = 'user'
    @field_validator("access_token")
    def hexlify_token(cls, value):
        """ Конвертирует UUID в hex строку """
        return value.hex
    class Config:
        from_attributes = True

class User(BaseModel):
    """Формирует тело ответа с деталями пользователя и токеном"""
    id: int
    role: str
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    patronymic: Optional[str] = None
    address: Optional[UserAddress] = None
    
    class Config:
        from_attributes = True