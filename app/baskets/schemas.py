from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime



class IBasketItem(BaseModel):
    product_id: int  = None
    amount: int  = None
    price: int  = None
    preview_img: Optional[str] = None
    title: Optional[str] = None
    category_name: Optional[str] = None
    brand: Optional[str] = None
    old_price: Optional[int] = None
    price: Optional[int] = None 
    is_hit: Optional[bool] = None
    article: Optional[str] = None



class IBasketBase(BaseModel):
    user_id: Optional[UUID] = None
    updated_date: datetime = datetime.now()


class IBasketItemChange(BaseModel):
    product_id: int
    amount: int

class IBasketCreate(IBasketBase):
    pass

    
class IBasket(IBasketBase):
    id: Optional[int] = None
    items: Optional[List[IBasketItem]] = None




class IOrderInfo(BaseModel):
    shipping_method: str
    phone: str
    name: str
    surname: str
    patronymic: str
    region: Optional[str]
    city: Optional[str]
    street: Optional[str]
    num_of_house: Optional[str]
    postcode: Optional[int]
    ids: Optional[List[int]]
    
class IOrderResponse(BaseModel):
    message: str