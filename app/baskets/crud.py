from typing import List
from uuid import UUID
from fastapi import Depends
from app.auth.models import User
from app.baskets.schemas import IBasket, IBasketCreate, IBasketItem, IBasketItemChange
from app.utils.base_crud import CRUDBase
from .models import Basket, BasketItem
from app.products.models import  Product

from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload
from app.db.session import async_session_maker

class CRUDBasket(CRUDBase[Basket, IBasketCreate, IBasketCreate]):
    async def get_by_user_id(self, user_id: UUID) -> IBasket:
        async with async_session_maker() as db_session:
            query = (
                select(Basket)
                .options(joinedload(Basket.items).joinedload(BasketItem.product).joinedload(Product.category))
                .where(self.model.user_id == user_id)
            )
            response = await db_session.execute(query)
            basket = response.scalars().first()
            
            if not basket:
                return None

            # Преобразование данных в Pydantic модели
            items = [
                IBasketItem(
                    id=item.id,
                    basket_id=item.basket_id,
                    product_id=item.product_id,
                    amount=item.amount,
                    article=item.product.article if item.product.article else None,
                    price=item.product.price if item.product.price else None,
                    title=item.product.title if item.product.title else None ,
                    category_name=item.product.category.name if item.product.category.name else None,
                    brand=item.product.brand if item.product.brand else None,
                    old_price=item.product.old_price if item.product.old_price else None,
                    is_hit=item.product.is_hit if item.product.is_hit else False,
                    is_sale=bool(item.product.old_price) if item.product.old_price is not None else False,
                    preview_img=item.product.preview_img if item.product.preview_img else None
                )
                for item in basket.items
            ]

            return IBasket(
                id=basket.id,
                user_id=basket.user_id,
                updated_date=basket.updated_date,
                items=items
            )

    async def change_basket_item(self, item: IBasketItemChange, basket_id: int):
        async with async_session_maker() as db_session:
            # Проверяем, есть ли элемент с данным product_id в корзине
            query = select(BasketItem).where(BasketItem.product_id==item.product_id and BasketItem.basket_id==basket_id)
            response = await db_session.execute(query)
            basket_item = response.scalars().first()
            
            if basket_item:
                if item.amount == 0:
                    await db_session.delete(basket_item)
                else:
                    # Если элемент найден, изменяем его количество
                    basket_item.amount = item.amount
            else:
                # Если элемент не найден, добавляем его в корзину
                basket_item = BasketItem(
                    basket_id=basket_id,
                    product_id=item.product_id,
                    amount=item.amount
                )
                db_session.add(basket_item)

            # Сохраняем изменения в базе данных
            await db_session.commit()
            if item.amount == 0:
                return None
            await db_session.refresh(basket_item)
            return basket_item
    
    
    async def delete_basket_items(self, basket: Basket, ids: List[int]):
        async with async_session_maker() as db_session:
            query = (
                delete(BasketItem)
                .where(
                    BasketItem.product_id.in_(ids),
                    BasketItem.basket_id == basket.id
                )
            )
            # Выполняем запрос на удаление
            await db_session.execute(query)
            await db_session.commit()

crud_baskets = CRUDBasket(Basket)










