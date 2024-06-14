from typing import List, Optional

from fastapi import Query
from sqlalchemy import Select, Tuple

from app.products.models import Product
from app.products.schemas import IProductFilterParams
from app.categories.crud import crud_category

async def get_product_filter_params(
    min_price: Optional[float] = Query(None, description="Минимальная цена для фильтрации"),
    max_price: Optional[float] = Query(None, description="Максимальная цена для фильтрации"),
    brands: List[str] = Query(None, description="Список брендов для фильтрации"),
    categories: List[int] = Query(None, description="Список категорий для фильтрации принимает их id"),
    page: int = Query(1, description="Номер страницы пагинации"),
    page_limit: int = Query(12, description="Лимит страницы"),
    sort_by: Optional[str] = Query(None, description="Параметр сортировки (price, popularity, date)"),
    sort_order: str = Query("asc", description="Порядок сортировки (asc - по возрастанию, desc - по убыванию)"),
    is_hit: Optional[bool] = Query(None, description="Возвращает хит продукты"),
    is_new: Optional[bool] = Query(None, description="Возвращает новые продукты")
) -> IProductFilterParams:
    return IProductFilterParams(
        min_price=min_price,
        max_price=max_price,
        brands=brands,
        categories=categories,
        page=page,
        page_limit=page_limit,
        sort_by=sort_by,
        sort_order=sort_order,
        is_hit=is_hit,
        is_new=is_new
    )
    
async def apply_product_filter(query, params: IProductFilterParams):
    if params.min_price is not None:
        query = query.where(Product.price > params.min_price)

    if params.max_price is not None:
        query = query.where(Product.price <= params.max_price)
    if params.brands:
        query = query.where(Product.brand.in_(params.brands))
    if params.is_hit is not None:
        query = query.where(Product.is_hit == params.is_hit)
        
    if params.categories:
        categories = await crud_category.get_categories_id_with_children(params.categories)
        print(categories)
        query = query.filter(Product.category_id.in_(categories))
    return query
