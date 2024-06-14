from fastapi import Query, UploadFile, File
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import List, Optional

from app.products.models import Product
from app.utils.common_schema import PaginationList


class IProductProp(BaseModel):
    name: str
    value: Optional[str]
    model_config = ConfigDict(from_attributes=True)

class IImages(BaseModel):
    image_url: str
    alt: str
    model_config = ConfigDict(from_attributes=True)
    
class IFiles(BaseModel):
    file: str
    model_config = ConfigDict(from_attributes=True)
    

class IProductCreate(BaseModel):
    title: str
    preview_img: str
    category_id: Optional[int] = None
    sort: Optional[int] = 0
    old_price: Optional[int] = None
    price: int = None
    is_hit: bool = False
    brand: Optional[str] = None
    description: Optional[str] = None
    article: str = None
    properties: List[IProductProp]
    images: Optional[List[IImages]] = None
    files: Optional[List[IFiles]] = None


class IProductCreateByParser(IProductCreate):
    category_name: Optional[str] = Field(None, description="Указывается либо category_id, либо category_name")

class IProductUpdate(BaseModel):
    title: Optional[str] = None
    preview_img: Optional[str] = None
    category_id: Optional[int] = None
    sort: Optional[int] = 0
    old_price: Optional[int] = None
    price: Optional[int] = None
    is_hit: Optional[bool] = None
    brand: Optional[str] = None
    description: Optional[str] = None
    article: str = None


class IProductPreview(BaseModel):
    id: int = None
    preview_img: Optional[str] = None
    title: Optional[str] = None
    category_name: Optional[str] = None
    brand: Optional[str] = None
    old_price: Optional[int] = None
    price: Optional[int] = None 
    is_hit: Optional[bool] = None

    @classmethod
    def from_orm(cls, product: Product):
        # Создаем объект IProduct из существующего объекта Product
        product_data = cls.model_validate(product.__dict__)
        # Обновляем его с помощью поля category_name
        return product_data.model_copy(update={"category_name": product.category.name if product.category else None})
    


class IProduct(BaseModel):
    id: int
    title: str
    preview_img: str
    category_id: Optional[int] = None
    category_name: Optional[str] = None
    sort: Optional[int] = 0
    old_price: Optional[int] = None
    price: int = None
    is_hit: bool = False
    brand: Optional[str] = None
    description: Optional[str] = None
    article: str = None
    properties: Optional[List[IProductProp]] = None
    images: Optional[List[IImages]] = None
    files: Optional[List[IFiles]] = None
    
    
    @classmethod
    def from_orm(cls, product: Product):
        # Создаем объект IProduct из существующего объекта Product
        product_data = cls.model_validate(product.__dict__)
        # Обновляем его с помощью поля category_name
        return product_data.model_copy(update={"category_name": product.category.name if product.category else None})
    
    
    model_config = ConfigDict(from_attributes=True)


        
class IProductSearch(BaseModel):
    id: int = None
    preview_img: Optional[str] = None
    title: Optional[str] = None
    category_name: Optional[str] = None
    brand: Optional[str] = None
    old_price: Optional[int] = None
    price: Optional[int] = None 
    is_hit: Optional[bool] = None
    article: Optional[str] = None
    description: Optional[str] = None

    @classmethod
    def from_orm(cls, product: Product):
        # Создаем объект IProduct из существующего объекта Product
        product_data = cls.model_validate(product.__dict__)
        # Обновляем его с помощью поля category_name
        return product_data.model_copy(update={"category_name": product.category.name if product.category else None})
    


class IProductList(PaginationList):
    products: List[IProductPreview]

class IProductSeacrhList(PaginationList):
    products: List[IProductSearch]
    
    
class IProductFilterParams(BaseModel):
    min_price: Optional[float] = Field(None, description="Минимальная цена для фильтрации")
    max_price: Optional[float] = Field(None, description="Максимальная цена для фильтрации")
    brands: List[str] = Field(None, description="Список брендов для фильтрации")
    categories: List[int] = Field(None, description="Список категорий для фильтрации принимает их id")
    page: int = Field(1, description="Номер страницы пагинации")
    page_limit: int = Field(12, description="Лимит страницы")
    sort_by: Optional[str] = Field(None, description="Параметр сортировки (price, popularity, date)")
    sort_order: str = Field("asc", description="Порядок сортировки (asc - по возрастанию, desc - по убыванию)")
    is_hit: Optional[bool] = Field(None, description="Возвращает хит продукты")
    is_new: Optional[bool] = Field(None, description="Возвращает новые продукты")
