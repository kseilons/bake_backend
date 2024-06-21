
from typing import List
from fastapi import HTTPException
from sqlalchemy import or_, select
from sqlalchemy.orm import joinedload
from app.categories.deps import is_valid_category_id
from app.products.utils import apply_product_filter
from .crud import crud_product
from .models import Product
from .schemas import IProductCreate, IProductFilterParams, IProductPreview, IProductPriceUpdate, IProductSearch, IProductUpdate, IProduct

async def create(catalog: IProductCreate):
    product = await crud_product.create(obj_in=catalog)
    return IProduct.from_orm(product)

async def get_by_id(product_id: int):
    product = await crud_product.get(id=product_id)
    return IProduct.from_orm(product)

async def update(
    product: Product,
    product_new: IProductUpdate
):      
    if product_new.category_id:
        await is_valid_category_id(product_new.category_id)  
    product = await crud_product.update(obj_current=product, obj_new=product_new)
    return IProduct.from_orm(product)


async def update_prices(
    product_prices: List[IProductPriceUpdate]
):  
    failed_articles = []
    for product_price in product_prices:
        success = await crud_product.update_price(product_price)
        if not success:
            failed_articles.append(product_price.article)
    return {
        "status": "success",
        "message": "Prices updated successfully",
        "failed_articles": failed_articles
    }
    
    
async def update_price(
    product_price: IProductPriceUpdate
):  
    success = await crud_product.update_price(product_price)
    if not success:
        raise HTTPException(status_code=500, detail={
            "status": "failed",
            "message": "Price update failed",
            "failed_articles": product_price.article
        })
    return {
        "status": "success",
        "message": "Price updated successfully",
        "failed_articles": None
    }


async def delete(catalog_id: int):
    return await crud_product.remove(id=catalog_id)



async def get_multi_filtered(params: IProductFilterParams,):
    query = (
        select(
            Product,
        )
        .options(joinedload(Product.properties),\
                        joinedload(Product.images),\
                        joinedload(Product.files),\
                        joinedload(Product.category))
    )
    query = await apply_product_filter(query, params)
    skip = (params.page - 1) * params.page_limit
    result = await crud_product.get_multi_ordered(query=query, 
                                                    skip= skip,
                                                    limit=params.page_limit,
                                                    order=params.sort_order, 
                                                    order_by=params.sort_by)
    products = [IProductPreview.from_orm(product) for product in result['data']]
    return {"products": products, "total_pages": result['total_pages'], "total_count": result['total_count']}


async def get_multi_search(search: str, page_limit: int = 10, page: int = 0):
    query = (
        select(
            Product,
        )
        .options(joinedload(Product.properties),\
                        joinedload(Product.images),\
                        joinedload(Product.files),\
                        joinedload(Product.category))
    )
    search_pattern = f"%{search}%"
    query = query.where(
        or_(
            Product.title.ilike(search_pattern),
            Product.description.ilike(search_pattern),
            Product.article.ilike(search_pattern),
            Product.brand.ilike(search_pattern)
        )
    )
    skip = (page - 1) * page_limit
    result = await crud_product.get_multi_ordered(query=query, 
                                                    skip= skip,
                                                    limit=page_limit)
    products = [IProductSearch.from_orm(product) for product in result['data']]
    return {"products": products, "total_pages": result['total_pages'], "total_count": result['total_count']}
