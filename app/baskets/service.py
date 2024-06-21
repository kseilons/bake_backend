

from uuid import UUID
from fastapi import HTTPException
from requests import Session
from app.auth.models import User
from app.baskets.crud import crud_baskets 
from app.baskets.models import Basket 
from app.baskets.schemas import IBasket, IBasketCreate, IBasketItemChange, IOrderInfo, IOrderResponse
from app.utils.email.smtp_server import email_sender
from app.core.config import settings
from app.utils.email.template_renderer import render_template

async def get(user_id: UUID):
    basket = await crud_baskets.get_by_user_id(user_id)
    if not basket:
        basket_create = IBasketCreate(user_id=user_id)
        basket = await crud_baskets.create(obj_in=basket_create)
        basket = await crud_baskets.get_by_user_id(user_id)
    return basket


async def change_basket_item(item: IBasketItemChange, 
                            user_id: UUID,
    ):
    basket = await get(user_id)
    basket_item = await crud_baskets.change_basket_item(item=item, basket_id=basket.id)
    if basket_item is None:
        return {"message": "Basket item deleted"}
    return basket_item


async def process_order(order_info: IOrderInfo,user: User ):
    basket = await crud_baskets.get_by_user_id(user.id)
    if not basket.items:
        raise HTTPException(status_code=400, detail="Корзина пуста. Невозможно оформить заказ.")
    
    await send_email_for_manager(order_info, user, basket)
    await send_email_for_user(order_info, user, basket)
    
    # await crud_baskets.delete_basket_items(basket, order_info.ids)
    return IOrderResponse(message="Заказ успешно оформлен.")
    
    
async def send_email_for_manager(order_info: IOrderInfo, user: User, basket: Basket):
    context = {
        "shipping_method": order_info.shipping_method,
        "user_phone": order_info.phone,
        "user_email": user.email,
        "user_name": order_info.name,
        "user_surname": order_info.surname,
        "user_patronymic": order_info.patronymic,
        "area": order_info.area,
        "region": order_info.region,
        "street": order_info.street,
        "city": order_info.city,
        "num_of_house": order_info.num_of_house,
        "postcode": order_info.postcode,
        "sum": 0,
        "basket": []
    }
    products_url = settings.FRONTEND_URL
    for item in basket.items:
        if (item.product_id in (order_info.ids)):
            context['sum'] += item.price
            context['basket'].append({
                "product_href": f"{products_url}/products/{item.product_id}",
                "product_name": item.title,
                "product_article": item.article,
                "product_brand": item.brand,
                "product_amount": item.amount,
                "product_price": item.price,
                "product_preview_img": item.preview_img
            })
    
    html_content = render_template(settings.template.ORDER_FOR_MANAGER, context)
    # Отправка письма с подтверждением
    await email_sender.send_email(
        email_to=settings.email.MANAGER_EMAIL,
        subject='Пользователь сделал заказ',
        body=html_content
    )

    
async def send_email_for_user(order_info: IOrderInfo, user: User, basket: Basket):
    context = {
        "shipping_method": order_info.shipping_method,
        "user_phone": order_info.phone,
        "user_email": user.email,
        "user_name": order_info.name,
        "user_surname": order_info.surname,
        "user_patronymic": order_info.patronymic,
        "area": order_info.area,
        "region": order_info.region,
        "street": order_info.street,
        "city": order_info.city,
        "num_of_house": order_info.num_of_house,
        "postcode": order_info.postcode,
        "sum": 0,
        "basket": []
    }
    products_url = settings.FRONTEND_URL
    for item in basket.items:
        if (item.product_id in (order_info.ids)):
            context['sum'] += item.price
            context['basket'].append({
                "product_href": f"{products_url}/products/{item.product_id}",
                "product_name": item.title,
                "product_article": item.article,
                "product_brand": item.brand,
                "product_amount": item.amount,
                "product_price": item.price,
                "product_preview_img": item.preview_img
            })
    
    html_content = render_template(settings.template.ORDER_FOR_USER, context)
    # Отправка письма с подтверждением
    await email_sender.send_email(
        email_to=user.email,
        subject='Ваш заказ',
        body=html_content
    )