

from fastapi import HTTPException
from requests import Session
from app.schemas import baskets as basket_schemas
from app.schemas import users as users_schemas
from app.crud import baskets as crud_baskets
from app.models.baskets import Basket 
from app.utils.email.smtp_server import email_sender
from app.setting import manager_email
from app.utils.email.template_renderer import render_template

async def get_basket(user_id: int, db: Session):
    basket = await crud_baskets.get_basket_by_user_id(user_id, db)
    if not basket:
        basket = await crud_baskets.create_basket(user_id, db)
    
    return basket


async def change_basket_item(item: basket_schemas.BasketItemChange, 
                            user_id: users_schemas.User,
                            db: Session):
    basket = await get_basket(user_id, db)
    basket_item = await crud_baskets.change_basket_item(item, basket.id, db)
    await crud_baskets.update_basket_timestamp(basket, db)
    return basket_item


async def order_basket(order_info: basket_schemas.OrderInfo,current_user: users_schemas.User , db: Session):
    basket = await get_basket(current_user.id, db)
    if not basket.items:
        raise HTTPException(status_code=400, detail="Корзина пуста. Невозможно оформить заказ.")
    
    await send_email_for_manager(order_info, current_user, basket)
    await send_email_for_user(order_info, current_user, basket)
    
    await crud_baskets.delete_basket_items(basket, db)
    return basket_schemas.OrderResponse(message="Заказ успешно оформлен.")
    
    
async def send_email_for_manager(order_info: basket_schemas.OrderInfo, current_user: users_schemas.User, basket: Basket):
    context = {
        "shipping_method": order_info.shipping_method,
        "user_phone": order_info.phone,
        "user_email": current_user.email,
        "user_name": order_info.name,
        "user_surname": order_info.surname,
        "user_patronymic": order_info.patronymic,
        "region": order_info.user_address.region,
        "city": order_info.user_address.city,
        "num_of_house": order_info.user_address.num_of_house,
        "postcode": order_info.user_address.postcode,
        "basket": []
    }
    for item in basket.items:
        context['basket'].append({
            "product_name": item.product.title,
            "product_article": item.product.info[0].article if item.product.info else None,
            "product_brand": item.product.brand,
            "product_price": item.product.price,
            "product_preview_img": item.product.preview_img
        })
    
    html_content = render_template('completed_order.html', context)
    # Отправка письма с подтверждением
    await email_sender.send_email(
        email_to=manager_email,
        subject='Пользователь сделал заказ',
        body=html_content
    )

    
async def send_email_for_user(order_info: basket_schemas.OrderInfo, current_user: users_schemas.User, basket: Basket):
    context = {
        "shipping_method": order_info.shipping_method,
        "user_phone": order_info.phone,
        "user_email": current_user.email,
        "user_name": order_info.name,
        "user_surname": order_info.surname,
        "user_patronymic": order_info.patronymic,
        "region": order_info.user_address.region,
        "city": order_info.user_address.city,
        "num_of_house": order_info.user_address.num_of_house,
        "postcode": order_info.user_address.postcode,
        "basket": []
    }
    for item in basket.items:
        context['basket'].append({
            "product_name": item.product.title,
            "product_article": item.product.info[0].article if item.product.info else None,
            "product_brand": item.product.brand,
            "product_price": item.product.price,
            "product_preview_img": item.product.preview_img
        })
    
    html_content = render_template('order_for_user.html', context)
    # Отправка письма с подтверждением
    await email_sender.send_email(
        email_to=current_user.email,
        subject='Ваш заказ',
        body=html_content
    )