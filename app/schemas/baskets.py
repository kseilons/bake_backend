from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class BasketItem(BaseModel):
    product_id: int
    amount: int


class BasketBase(BaseModel):
    id_user: Optional[int] = None
    updated_date: datetime = datetime.now()
    basket_items: List[BasketItem]


class BasketItemChange(BaseModel):
    user_id: Optional[int] = None
    basket_item: BasketItem



class Basket(BasketBase):
    id: int

    class Config:
        orm_mode = True
