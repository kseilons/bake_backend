
from app.categories.crud import crud_category
from app.categories.schemas import ICategoryCreate
from app.categories.utils import get_level_nesting

async def create(catalog: ICategoryCreate):
    catalog.level_nesting = await get_level_nesting(catalog.parent_id)
    catalog.parent_id = None if catalog.parent_id == 0 else catalog.parent_id
    return await crud_category.create(obj_in=catalog)