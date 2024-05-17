from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas import baskets as schemas
from app.crud import baskets as controllers
from app.models.database import get_db

router = APIRouter()


@router.get("/basket", response_model=List[schemas.BasketItem])
async def get_basket(user_id: int, db: Session = Depends(get_db)):
    basket = controllers.get_basket_by_user_id(user_id, db)
    if not basket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Basket not found")
    return basket.basket_items


@router.post("/basket", response_model=schemas.BasketItem)
async def change_basket_item(item: schemas.BasketItemChange, db: Session = Depends(get_db)):
    basket_item = controllers.change_basket_item(item, db)
    return basket_item




