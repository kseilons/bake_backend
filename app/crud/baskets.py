from requests import Session
from sqlalchemy import func

from app.auth.models import Users
from app.schemas import baskets as basket_schemas
from app.models.baskets import Basket, BasketItem



async def get_basket_by_user_id(user_id: int, db: Session):
    """ Возвращает корзину по id пользователя """
    return db.query(Basket).filter_by(user_id=user_id).first()


async def create_basket(user_id: int, db: Session):
    """Создает корзину для пользователя и возвращает созданную корзину"""
    new_basket = Basket(user_id=user_id)
    db.add(new_basket)
    db.commit()
    db.refresh(new_basket)
    return new_basket


async def change_basket_item(item: basket_schemas.BasketItemChange, basket_id: int, db: Session):
    # Проверяем, есть ли элемент с данным product_id в корзине
    basket_item = db.query(BasketItem).filter_by(product_id=item.product_id, basket_id=basket_id).first()

    if basket_item:
        # Если элемент найден, изменяем его количество
        basket_item.amount = item.amount
    else:
        # Если элемент не найден, добавляем его в корзину
        basket_item = BasketItem(
            basket_id=basket_id,
            product_id=item.product_id,
            amount=item.amount
        )
        db.add(basket_item)

    # Сохраняем изменения в базе данных
    db.commit()
    db.refresh(basket_item)

    return basket_item



async def update_basket_timestamp(basket: Basket, db: Session):
    basket.updated_date = func.now()
    db.commit()
    db.refresh(basket)
    return basket


async def delete_basket_items(basket: Basket, db: Session):
    if basket and basket.items:
        for item in basket.items:
            db.delete(item)
        db.commit()