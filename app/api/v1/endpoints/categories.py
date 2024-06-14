
from app.categories.deps import category_exists, is_valid_category, is_valid_category_id
from app.categories.schemas import ICategoryCreate, ICategoryResponse, ICategoryUpdate, ICategoryWithChildrenResponse
from fastapi import APIRouter, Depends, status

from app.categories.crud import crud_category
from app.categories import service
from app.auth.models import User
from app.auth.auth import current_superuser
router = APIRouter(tags=['categories'])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_catalog(catalog: ICategoryCreate = Depends(category_exists),
                        user: User = Depends(current_superuser),
                        ) -> ICategoryResponse:
    """
        Этот метод создает сущность категории. В sort чем больше значение, тем выше приоритет у каталога
    """
    return await service.create(catalog=catalog)


@router.get("/")
async def get_categories(parent_id: int = 0,
                        deep_level: int = 2
                        ) -> list[ICategoryWithChildrenResponse]:
    """
    Возвращает каталоги из базы данных.
    Если parent_id = 0, возвращает корневые каталоги.
    Параметр deep_level определяет количество уровней вложенности.
    """
    return await service.get_with_child(parent_id, deep_level)

@router.put("/{category_id}")
async def update_category(
        category_new: ICategoryUpdate,
        category: int = Depends(is_valid_category),
        user: User = Depends(current_superuser)
):
    """
        Обновляет значения указанные в теле запроса.
    """
    return await service.update(category, category_new)



@router.delete("/{category_id}")
async def delete_catalog(
        category_id: int = Depends(is_valid_category_id),
        current_user: User = Depends(current_superuser)
) -> ICategoryWithChildrenResponse:
    """
        Удаляет каталог.
    """
    return await crud_category.remove(id=category_id)
