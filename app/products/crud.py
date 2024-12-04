
from logging import getLogger
from typing import Any
from fastapi import Depends, HTTPException
from psycopg2 import IntegrityError
from app.auth.models import User
from app.categories.models import Category
from app.utils.base_crud import CRUDBase
from .schemas import IProductCreate, IProduct, IProductPriceUpdate, IProductUpdate
from .models import Product, ProductFile, ProductImage, ProductProperty

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.db.session import async_session_maker
from sqlalchemy import select,  exc, select

logger = getLogger()

class CRUDProduct(CRUDBase[Product, IProductCreate, IProductUpdate]):
    async def get_by_title(self, title: str):
        async with async_session_maker() as db_session:
            query = select(self.model).where(self.model.title == title)
            response = await db_session.execute(query)
            return response.scalars().one_or_none()
        
    async def get(self, *, id: int) -> Product | None:
        logger.debug(f"Get product with id = {id}")
        async with async_session_maker() as db_session:
            query = select(Product)\
                .options(joinedload(Product.properties),\
                        joinedload(Product.images),\
                        joinedload(Product.files),\
                        joinedload(Product.category))\
                .where(self.model.id==id)
            response = await db_session.execute(query)
            return response.scalars().first()
        
    async def get_test(self, *, id: int) -> Product | None:
        logger.debug(f"Get product with id = {id}")
        async with async_session_maker() as db_session:
            query = select(Product)\
                .options(joinedload(Product.properties),\
                        joinedload(Product.images),\
                        joinedload(Product.files),\
                        joinedload(Product.category))\
                .where(self.model.id==id)
            response = await db_session.execute(query)
            return response.scalars().first()
        
        
    async def create(
        self,
        *,
        obj_in: IProductCreate 
    ) -> Product:
        async with async_session_maker() as db_session:
            product_data = obj_in.model_dump(exclude={"properties", "images", "files"})

            db_obj = self.model(**product_data)

            try:
                db_session.add(db_obj)
                await db_session.commit()
                await db_session.refresh(db_obj)
                # Process properties
                if obj_in.properties:
                    db_properties = [
                        ProductProperty(
                            prod_id=db_obj.id,
                            name=property.name,
                            value=property.value
                        ) for property in obj_in.properties
                    ]
                    db_session.add_all(db_properties)
                # Process images
                if obj_in.images:
                    db_images = [
                        ProductImage(
                            product_id=db_obj.id,
                            image_url=image.image_url,
                            alt=image.alt
                        ) for image in obj_in.images
                    ]
                    db_session.add_all(db_images)
            
                # Process files
                if obj_in.files:
                    db_files = [
                        ProductFile(
                            product_id=db_obj.id,
                            file=file.file
                        ) for file in obj_in.files
                    ]
                    db_session.add_all(db_files)
                    
                await db_session.commit()
                
                return await self.get(id=db_obj.id)
                
            except exc.IntegrityError as e:
                logger.debug(e)
                await db_session.rollback()
                raise HTTPException(
                    status_code=409,
                    detail="Resource already exists",
                ) from e

    async def update(
        self,
        *,
        obj_current: Product,
        obj_new: IProductUpdate | dict[str, Any] | Product
    ) -> Product:
        async with async_session_maker() as db_session:

            if isinstance(obj_new, dict):
                update_data = obj_new
            else:
                update_data = obj_new.model_dump(
                    exclude_unset=True
                )  # This tells Pydantic to not include the values that were not sent
            for field in update_data:
                setattr(obj_current, field, update_data[field])
            try:
                db_session.add(obj_current)
                await db_session.commit()
            except exc.IntegrityError as e:
                await db_session.rollback()
                raise HTTPException(
                    status_code=409,
                    detail="Product with this title already exist",
                ) from e
            await db_session.commit()
            return await self.get(id=obj_current.id)
        
        
    async def update_price(self, product_update: IProductPriceUpdate) -> bool:
        async with async_session_maker() as db_session:
            query = select(Product).where(Product.article == product_update.article)
            result = await db_session.execute(query)
            product = result.scalar_one_or_none()
            
            if not product:
                return False
            
            if product.price != product_update.price:
                if product.old_price: 
                    if product_update.price >= product.old_price:
                        product.old_price = None
                    else:
                        product.old_price = product.price
                product.price = product_update.price
                
                try:
                    db_session.add(product)
                    await db_session.commit()
                except IntegrityError as e:
                    await db_session.rollback()
                    return False
        return True


crud_product = CRUDProduct(Product)
