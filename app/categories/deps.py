from typing import Annotated

from fastapi import HTTPException, Path, status
from app.categories.models import Category

from app.categories.schemas import ICategoryCreate, ICategoryResponse
from app.utils.exceptions.common_exception import IdNotFoundException
from app.categories.crud import crud_category

async def is_valid_category_id(
    category_id: Annotated[int, Path(title="The UUID id of the user")]
) -> int:
    category = await crud_category.get(id=category_id)
    if not category:
        raise IdNotFoundException(Category, id=category_id)

    return category_id


async def is_valid_category(
    category_id: Annotated[int, Path(title="The UUID id of the user")]
) -> Category:
    category = await crud_category.user.get(id=category_id)
    if not category:
        raise IdNotFoundException(Category, id=category_id)

    return category


async def category_exists(new_category: ICategoryCreate) -> ICategoryCreate:
    user = await crud_category.get_by_name(name=new_category.name)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="There is already a catalog with same name",
        )
    return new_category