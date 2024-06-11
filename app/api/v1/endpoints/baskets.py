from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas import baskets as basket_schemas
from app.auth import schemas as users_schemas
from app.controller import baskets as basket_controller
from app.auth.auth import current_active_user
router = APIRouter(tags=['basket'])


@router.get("/", response_model=basket_schemas.Basket)
async def get_basket(current_user: users_schemas.User = Depends(current_active_user)):
    return await basket_controller.get_basket(current_user.id, db)


@router.put("/", response_model=basket_schemas.BasketItem)
async def change_basket_item(item: basket_schemas.BasketItemChange, 
                            current_user: users_schemas.User = Depends(get_current_user),
                            db: Session = Depends(get_db)):
    return await basket_controller.change_basket_item(item, current_user.id, db)


@router.post("/order/")
async def order_basket(order_info: basket_schemas.OrderInfo,
                    current_user: users_schemas.User = Depends(get_current_user), 
                    db: Session = Depends(get_db)):
    return await basket_controller.order_basket(order_info, current_user, db)