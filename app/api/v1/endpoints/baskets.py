from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Union

from app.baskets.models import Basket
from app.baskets.schemas import IBasket, IBasketItem, IBasketItemChange, IOrderInfo
from app.baskets import service
from app.auth.models import User
from app.auth.auth import current_active_user
router = APIRouter(tags=['basket'])


@router.get("/")
async def get_basket(user: User = Depends(current_active_user)
    ) -> IBasket:
    return await service.get(user.id)


@router.put("/")
async def change_basket_item(item: IBasketItemChange, 
                            user: User = Depends(current_active_user)
                            ) -> Union[IBasketItemChange, dict]:
    return await service.change_basket_item(item, user.id)


@router.post("/order/")
async def process_order(order_info: IOrderInfo,
                    user: User = Depends(current_active_user)):
    return await service.process_order(order_info, user)