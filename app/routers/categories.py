from app.schemas import categories as schemas
from app.crud import categories as controller
from app.models.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.schemas.users import User
from app.utils.dependecies import verify_admin_user

router = APIRouter(tags=['categories'])


@router.post("/", response_model=schemas.CategoryChangeResponse, status_code=status.HTTP_201_CREATED)
async def create_catalog(catalog: schemas.CategoryCreate, db: Session = Depends(get_db),
                         current_user: User = Depends(verify_admin_user)):
    """
        Этот метод создает сущность категории. В sort чем больше значение, тем выше приоритет у каталога
    """
    result = await controller.create_category(db, catalog)
    return result





@router.get("/", response_model=schemas.CategoryList)
async def get_categories(parent_id: int = 0,
                         deep_level: int = 2,
                         db: Session = Depends(get_db)):
    """
    Возвращает каталоги из базы данных.
    Если parent_id = 0, возвращает корневые каталоги.
    Параметр deep_level определяет количество уровней вложенности.
    """
    result = await controller.get_categories(db, parent_id, deep_level)

    return result


@router.put("/{category_id}", response_model=schemas.CategoryChangeResponse)
async def update_category(
        category_id: int, category: schemas.CategoryUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(verify_admin_user)
):
    """
        Обновляет значения указанные в теле запроса.
    """
    return await controller.update_catalog(db, category_id=category_id, category=category)


@router.put("/{category_id}/change_sort_order", response_model=schemas.CategoryChangeResponse, status_code=status.HTTP_200_OK)
async def change_category_sort_order(
        category_id: int,
        sort_order: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(verify_admin_user)
):
    """
    Изменяет порядок сортировки категории по её идентификатору.
    """
    category = await controller.update_category_sort_order(db, category_id, sort_order)
    return category


@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
async def delete_catalog(
        category_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(verify_admin_user)
):
    """
        Удаляет каталог, если нет связанных продуктов
    """
    return await controller.delete_catalog(db, category_id=category_id)
