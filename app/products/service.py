
from app.categories.deps import is_valid_category_id
from .crud import crud_product
from .models import Product
from .schemas import IProductCreate, IProductFilterParams, IProductUpdate, IProduct

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

async def delete(catalog_id: int):
    return await crud_product.remove(id=catalog_id)



async def get_multi_filtered(params: IProductFilterParams):
    query = (
        select(
            Product,
        )
        .join(UserFollow, User.id == UserFollow.user_id)
        .where(UserFollow.target_user_id == current_user.id)
    )
    return await crud_product.get_multi_paginated(params=params, query=query)

