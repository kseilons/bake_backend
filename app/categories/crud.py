
from fastapi import Depends
from app.auth.models import User
from app.utils.base_crud import CRUDBase
from .schemas import ICategoryCreate, ICategoryResponse, ICategoryUpdate
from .models import Category

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import async_session_maker

class CRUDCategory(CRUDBase[Category, ICategoryCreate, ICategoryUpdate]):
    pass


crud_category = CRUDCategory(Category)