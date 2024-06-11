
from fastapi import Depends
from app.auth.models import User
from app.utils.base_crud import CRUDBase
from .schemas import ICategoryCreate, ICategoryResponse, ICategoryUpdate
from .models import Category

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.db.session import async_session_maker

class CRUDCategory(CRUDBase[Category, ICategoryCreate, ICategoryUpdate]):
    async def get_by_parent_id(self, id: int):
        async with async_session_maker() as db_session:
            query = select(self.model).options(joinedload(Category.children)).where(self.model.parent_id == id)
            response = await db_session.execute(query)
            return response.scalars().unique()
        
    async def get_by_name(self, name: str):
        async with async_session_maker() as db_session:
            query = select(self.model).where(self.model.name == name)
            response = await db_session.execute(query)
            return response.scalars().one_or_none()

crud_category = CRUDCategory(Category)