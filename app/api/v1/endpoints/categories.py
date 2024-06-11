
from app.categories.schemas import ICategoryCreate, ICategoryResponse
from fastapi import APIRouter, Depends, status

from app.categories.crud import crud_category
from app.categories import service
from app.auth.models import User
from app.auth.auth import current_active_user, current_superuser
router = APIRouter(tags=['categories'])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_catalog(catalog: ICategoryCreate,
                        user: User = Depends(current_superuser),
                        ) -> ICategoryResponse:
    """
        Этот метод создает сущность категории. В sort чем больше значение, тем выше приоритет у каталога
    """
    return await service.create(catalog=catalog)


@router.get("/", response_model=list[ICategoryResponse])
async def get_categories(parent_id: int = 0,
                        deep_level: int = 2):
    """
    Возвращает каталоги из базы данных.
    Если parent_id = 0, возвращает корневые каталоги.
    Параметр deep_level определяет количество уровней вложенности.
    """
    
    result = await crud_category.get_multi()

    return result





# @router.put("/{category_id}", response_model=schemas.CategoryChangeResponse)
# async def update_category(
#         category_id: int, category: schemas.ICategoryUpdate,
#         db: Session = Depends(get_db),
#         current_user: User = Depends(verify_admin_user)
# ):
#     """
#         Обновляет значения указанные в теле запроса.
#     """
#     return await controller.update_catalog(db, category_id=category_id, category=category)


# @router.put("/{category_id}/change_sort_order", response_model=schemas.CategoryChangeResponse, status_code=status.HTTP_200_OK)
# async def change_category_sort_order(
#         category_id: int,
#         sort_order: int,
#         db: Session = Depends(get_db),
#         current_user: User = Depends(verify_admin_user)
# ):
#     """
#     Изменяет порядок сортировки категории по её идентификатору.
#     """
#     category = await controller.update_category_sort_order(db, category_id, sort_order)
#     return category


# @router.delete("/{category_id}", status_code=status.HTTP_200_OK)
# async def delete_catalog(
#         category_id: int,
#         db: Session = Depends(get_db),
#         current_user: User = Depends(verify_admin_user)
# ):
#     """
#         Удаляет каталог, если нет связанных продуктов
#     """
#     return await controller.delete_catalog(db, category_id=category_id)
