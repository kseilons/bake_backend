from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from app.schemas.users import UserAddress


class BasketItem(BaseModel):
    product_id: int
    amount: int
    class Config:
        from_attributes = True


class BasketBase(BaseModel):
    user_id: Optional[int] = None
    updated_date: datetime = datetime.now()
    items: Optional[List[BasketItem]] = None


class BasketItemChange(BasketItem):
    pass



class Basket(BasketBase):
    id: int

    class Config:
        from_attributes = True



class OrderInfo(BaseModel):
    shipping_method: str
    user_address: UserAddress
    phone: str
    name: str
    surname: str
    patronymic: str
    
    
class OrderResponse(BaseModel):
    message: str