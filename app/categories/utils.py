from typing import TypeVar
from fastapi import HTTPException
from app.categories.crud import crud_category
from sqlalchemy.orm import DeclarativeBase
from .models import Category
from app.utils.exceptions.common_exception import IdNotFoundException


ModelType = TypeVar("ModelType", bound=DeclarativeBase)

async def get_level_nesting(parent_id: int):
    if parent_id == 0:
        return 1  # Корневая категория
    parent_catalog = crud_category.get(id=parent_id)
    if parent_catalog is not None:
        return parent_catalog.level_nesting + 1
    else:
        raise IdNotFoundException(Category, id=parent_id)

