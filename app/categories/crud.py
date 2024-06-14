
from typing import List
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
        
    async def get_categories_id_with_children(self, categories: List[int]) -> List[Category]:
        result_categories = []
        async with async_session_maker() as db_session:
            async def find_children(category_id):
                children = await self.get_by_parent_id(category_id)
                for child in children:
                    result_categories.append(child.id)
                    await find_children(child.id)
           

            for category_id in categories:
                result_categories.append(category_id)
                await find_children(category_id)
                
        return result_categories

crud_category = CRUDCategory(Category)