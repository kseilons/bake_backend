from typing import Annotated

from fastapi import HTTPException, Path, status
from app.categories.deps import category_by_name, category_exists, is_valid_category_id
from app.products.models import Product

from app.products.schemas import IProductCreate, IProduct, IProductCreateByParser
from app.utils.exceptions.common_exception import IdNotFoundException
from .crud import crud_product
from app.categories.crud import crud_category
from app.categories.schemas import ICategoryCreate

async def is_valid_product_id(
    product_id: Annotated[int, Path(title="The UUID id of the product")]
) -> int:
    product = await crud_product.get(id=product_id)
    if not product:
        raise IdNotFoundException(Product, id=product_id)

    return product_id


async def is_valid_product(
    product_id: Annotated[int, Path(title="The UUID id of the product")]
) -> Product:
    product = await crud_product.get(id=product_id)
    if not product:
        raise IdNotFoundException(Product, id=product_id)

    return product


async def product_valid(new_category: IProductCreate) -> IProductCreate:
    product = await crud_product.get_by_title(title=new_category.title)
    if product:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There is already a product with same title",
        )
    await is_valid_category_id(new_category.category_id)   
    return new_category


async def product_valid_by_parser(new_product: IProductCreateByParser) -> IProductCreate:
    category = await crud_category.get_by_name(name=new_product.category_name)
    if category is None:   
        category_create = ICategoryCreate(name=new_product.category_name)  
        if new_product.category_name_base == new_product.category_name:
            category_create.parent_id = None
        else:
            parent_category = await crud_category.get_by_name(name=new_product.category_name_base)
            if parent_category is None:
                raise HTTPException(
                    status_code=555,
                    detail="Category not found",
                )
            category_create.parent_id = parent_category.id
        category = await crud_category.create(obj_in=category_create)

    new_product.category_id = category.id
    product_data = new_product.model_dump(exclude={"category_name", "category_name_base"})
    return await product_valid(IProductCreate(**product_data))

