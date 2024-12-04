from os import environ
from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.config import settings

engine = create_async_engine(str(settings.database.DATABASE_URL))
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

metadata = MetaData()
class Base(DeclarativeBase):
    metadata = metadata
    
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
