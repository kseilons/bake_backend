
from app.categories.crud import crud_category
from app.categories.models import Category
from app.categories.schemas import ICategoryCreate, ICategoryUpdate, ICategoryWithChildrenResponse
from app.categories.utils import get_level_nesting
from app.utils.exceptions.common_exception import IdNotFoundException

async def create(catalog: ICategoryCreate):
    catalog.level_nesting = await get_level_nesting(catalog.parent_id)
    catalog.parent_id = None if catalog.parent_id == 0 else catalog.parent_id
    return await crud_category.create(obj_in=catalog)

async def get_with_child(
    parent_id: int = 0,
    deep_level: int = 2
):
    async def get_child_categories(parent_id: int, current_level: int):
        if current_level >= deep_level:
            return []
        db_categories = await crud_category.get_by_parent_id(parent_id)
        categories = []
        for db_category in db_categories:
            category = ICategoryWithChildrenResponse.model_validate(db_category)
            category.children = await get_child_categories(db_category.id, current_level + 1)
            categories.append(category)
        return categories

    if parent_id == 0:
        parent_id = None
    return await get_child_categories(parent_id, 0)


async def update(
    category: Category,
    category_new: ICategoryUpdate
):
    if category_new.parent_id == 0:
        category_new.parent_id = None
    if category_new.parent_id:
        if category_new.parent_id != category.parent_id:
            category_new.level_nesting = await get_level_nesting(category_new.parent_id)
        else:
            category_new.level_nesting = category.level_nesting
    return await crud_category.update(obj_current=category, obj_new=category_new)



