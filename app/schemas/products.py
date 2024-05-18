from fastapi import UploadFile, File
from pydantic import BaseModel, field_validator
from typing import List, Optional


class ProductProp(BaseModel):
    name: str
    value: Optional[str]
    class Config:
        from_attributes = True

class Images(BaseModel):
    image_url: str
    alt: str
    class Config:
        from_attributes = True
    
class Files(BaseModel):
    file: str
    

class ProductCreate(BaseModel):
    title: Optional[str] = None
    preview_img: str
    category_id: Optional[int] = None
    short_description: Optional[str] = None
    description: Optional[str] = None
    sort: Optional[int] = 0
    brand: Optional[str] = None
    old_price: int = None
    price: int = None
    is_hit: bool = False
    article: str = None
    properties: List[ProductProp]
    images: Optional[List[Images]] = None
    files: Optional[List[str]] = None
    @field_validator("short_description")
    def process_short_description(cls, v, values):
        """
        Валидатор для автоматического заполнения short_description, если он пустой.
        """
        if not v:
            return values.get("description")[:150]
        return v

class ProductCreateParser(ProductCreate):
    category_name: Optional[str]

class ProductUpdate(BaseModel):
    title: Optional[str] = None
    preview_img: Optional[str] = None
    category_id: Optional[str] = None
    short_description: Optional[str] = None
    description: Optional[str] = None
    sort: Optional[int] = None
    brand: str
    old_price: int = None
    price: int = None
    is_hit: bool = None
    article: str = None
    properties: Optional[List[ProductProp]] = None
    images: Optional[List[Images]] = None
    files: Optional[List[str]] = None


class ProductPreview(BaseModel):
    id: int = None
    preview_img: Optional[str] = None
    title: Optional[str] = None
    category_name: Optional[str] = None
    short_description: Optional[str] = None
    rating_avg: Optional[int] = None
    rating_count: Optional[int] = None
    brand: Optional[str] = None
    old_price: Optional[int] = None
    price: Optional[int] = None 
    is_hit: Optional[bool] = None

    class Config:
        from_attributes = True

    @classmethod
    def from_product(cls, product):
        return cls(
            id=product.id,
            title=product.title,
            category_name=product.category.name,
            short_description=product.short_description,
            rating_avg=product.rating_avg,
            rating_count=product.rating_count,
            brand=product.brand,
            old_price=product.old_price,
            price=product.price,
            is_hit=product.is_hit,
            preview_img=product.preview_img
        )


class Product(BaseModel):
    id: int
    title: Optional[str] = None
    category_name: Optional[str] = None
    description: Optional[str] = None
    rating_avg: Optional[int] = None
    rating_count: Optional[int] = None
    brand: Optional[str] = None
    old_price: Optional[int] = None
    price: Optional[int] = None
    is_hit: Optional[bool] = False
    article: Optional[str] = None
    properties: Optional[List[ProductProp]] = None
    images: Optional[List[Images]] = None
    files: Optional[List[Files]] = None

    class Config:
        from_attributes = True


class ProductList(BaseModel):
    products: List[ProductPreview]
    total_pages: int
    total_count: int



class Category(BaseModel):
    name: str
    class Config:
        from_attributes = True
        
class ProductSearch(BaseModel):
    id: int = None
    preview_img: Optional[str] = None
    title: Optional[str] = None
    category_name: Optional[str] = None
    rating_avg: Optional[int] = None
    rating_count: Optional[int] = None
    brand: Optional[str] = None
    old_price: Optional[int] = None
    price: Optional[int] = None 
    is_hit: Optional[bool] = None
    article: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


class ProductSearchList(BaseModel):
    products: List[ProductSearch]
    total_pages: int
    total_count: int