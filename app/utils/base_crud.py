from logging import getLogger
from fastapi import Depends, HTTPException
from typing import Any, Generic, TypeVar
from uuid import UUID

from requests import Session
from app.db.session import get_async_session
from app.utils.common_schema import IOrderEnum
from fastapi_pagination.ext.sqlmodel import paginate
from sqlalchemy.orm import DeclarativeBase
from fastapi_pagination import Params, Page
from pydantic import BaseModel
from sqlalchemy import insert, select, Select, exc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import async_session_maker

logger = getLogger()
ModelType = TypeVar("ModelType", bound=DeclarativeBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
SchemaType = TypeVar("SchemaType", bound=BaseModel)
T = TypeVar("T", bound=DeclarativeBase)



class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLModel model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, *, id: UUID | str) -> ModelType | None:
        async with async_session_maker() as db_session:
            query = select(self.model).where(self.model.id == id)
            response = await db_session.execute(query)
            return response.scalar_one_or_none()

    async def get_by_ids(
        self,
        *,
        list_ids: list[UUID | str]
    ) -> list[ModelType] | None:
        async with async_session_maker() as db_session:
            query = select(self.model).where(self.model.id.in_(list_ids))
            response = await db_session.execute(query)
            return response.scalars().all()

    async def get_count(self) -> ModelType | None:
        async with async_session_maker() as db_session:
            query = select(func.count()).select_from(select(self.model).subquery())
            response = await db_session.execute(query)
            return response.scalar_one()

    async def get_multi(
        self,
        *,
        skip: int = 0,
        limit: int = 12,
        query: T | Select[T] | None = None
    ) -> list[ModelType]:
        async with async_session_maker() as db_session:
            if query is None:
                query = select(self.model).offset(skip).limit(limit).order_by(self.model.id)
            response = await db_session.execute(query)
            return response.scalars().all()

    async def get_multi_paginated(
        self,
        *,
        params: Params | None = Params(),
        query: T | Select[T] | None = None
    ) -> Page[ModelType]:
        async with async_session_maker() as db_session:
            if query is None:
                query = select(self.model)
            return await paginate(db_session, query, params)

    async def get_multi_paginated_ordered(
        self,
        *,
        params: Params | None = Params(),
        order_by: str | None = None,
        order: IOrderEnum | None = IOrderEnum.asc,
        query: T | Select[T] | None = None,
    ) -> Page[ModelType]:
        async with async_session_maker() as db_session:
            columns = self.model.__table__.columns

            if order_by is None or order_by not in columns:
                order_by = "id"

            if query is None:
                if order == IOrderEnum.asc:
                    query = select(self.model).order_by(columns[order_by].asc())
                else:
                    query = select(self.model).order_by(columns[order_by].desc())

            return await paginate(db_session, query, params)

    async def get_multi_ordered(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        order_by: str | None = None,
        order: IOrderEnum | None = IOrderEnum.asc
    ) -> list[ModelType]:
        async with async_session_maker() as db_session:
            columns = self.model.__table__.columns

            if order_by is None or order_by not in columns:
                order_by = "id"

            if order == IOrderEnum.asc:
                query = (
                    select(self.model)
                    .offset(skip)
                    .limit(limit)
                    .order_by(columns[order_by].asc())
                )
            else:
                query = (
                    select(self.model)
                    .offset(skip)
                    .limit(limit)
                    .order_by(columns[order_by].desc())
                )

            response = await db_session.execute(query)
            return response.scalars().all()

    async def create(
        self,
        *,
        obj_in: CreateSchemaType | ModelType
    ) -> ModelType:
        async with async_session_maker() as db_session:
            db_session = db_session or self.db.session
            db_obj = self.model(**obj_in.model_dump())


            try:
                db_session.add(db_obj)
                await db_session.commit()
            except exc.IntegrityError as e:
                logger.debug(e)
                await db_session.rollback()
                raise HTTPException(
                    status_code=409,
                    detail="Resource already exists",
                ) from e
            await db_session.refresh(db_obj)
            return db_obj

    async def update(
        self,
        *,
        obj_current: ModelType,
        obj_new: UpdateSchemaType | dict[str, Any] | ModelType
    ) -> ModelType:
        async with async_session_maker() as db_session:

            if isinstance(obj_new, dict):
                update_data = obj_new
            else:
                update_data = obj_new.dict(
                    exclude_unset=True
                )  # This tells Pydantic to not include the values that were not sent
            for field in update_data:
                setattr(obj_current, field, update_data[field])

            db_session.add(obj_current)
            await db_session.commit()
            await db_session.refresh(obj_current)
            return obj_current

    async def remove(
        self, *, id: UUID | str
    ) -> ModelType:
        async with async_session_maker() as db_session:
            response = await db_session.exec(
                select(self.model).where(self.model.id == id)
            )
            obj = response.scalar_one()
            await db_session.delete(obj)
            await db_session.commit()
            return obj
