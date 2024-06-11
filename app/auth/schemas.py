from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, UUID4, Field, validator, field_validator

import uuid

from fastapi_users import schemas



class IUserCreate(schemas.BaseUserCreate):
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class IUserUpdate(schemas.BaseUserUpdate):
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None
    region: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    num_of_house: Optional[str] = None
    postcode: Optional[int] = None
    phone: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    patronymic: Optional[str] = None

class IUser(schemas.BaseUser[uuid.UUID]):
    id: uuid.UUID
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    region: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    num_of_house: Optional[str] = None
    postcode: Optional[int] = None
    phone: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    patronymic: Optional[str] = None