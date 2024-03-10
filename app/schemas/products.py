from pydantic import BaseModel
from typing import List, Optional


class ProductProp(BaseModel):
    prop_id: int
    value: int


class ProductCreate(BaseModel):
    title: str
    preview_img: str
    category_id: int
    short_description: Optional[str] = None
    description: str
    property: List[ProductProp]
    img: List[str]


class ProductUpdate(BaseModel):
    title: Optional[str] = None
    preview_img: Optional[str] = None
    category_id: Optional[str] = None
    short_description: Optional[str] = None
    description: Optional[str] = None
    property: Optional[List[ProductProp]] = None
    img: Optional[List[str]] = None


class ProductPreview(BaseModel):
    id: int
    title: str
    category_id: int
    short_description: str
    rating_avg: int
    rating_count: int

    class Config:
        orm_mode = True


class Product(BaseModel):
    id: int
    title: str
    category_name: str
    description: str
    property: List[ProductProp]
    img: List[str]
    rating_avg: int
    rating_count: int

    class Config:
        orm_mode = True


class ProductList(BaseModel):
    properties: List[ProductPreview]
