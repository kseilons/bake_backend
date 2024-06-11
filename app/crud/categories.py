from typing import List, Type

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.categories.models import Category as DBCategory
from app.categories import schemas as schemas
from fastapi import HTTPException, status

from app.utils.categories import get_level_nesting


async def create_category(db: Session, catalog: schemas.ICategoryCreate):
    parent_id = catalog.parent_id
    if parent_id == 0:
        parent_id = None  # Корневая категория
    db_category = DBCategory(
        name=catalog.name,
        parent_id=parent_id,
        sort=catalog.sort,
        level_nesting=get_level_nesting(db, catalog.parent_id),
    )

    db.add(db_category)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating catalog. {e.orig}"
        )

    db.refresh(db_category)
    return db_category

async def get_categories(db: Session, parent_id: int, deep_level: int):
    """
    Получает категории из базы данных в соответствии с указанным родительским идентификатором и уровнем вложенности.
    """

    def get_child_categories(parent_id, current_level):
        if current_level >= deep_level:
            return []
        db_categories = db.query(DBCategory).filter_by(parent_id=parent_id).order_by(-DBCategory.sort).all()
        categories = []
        for db_category in db_categories:
            category = schemas.Category.from_orm(db_category)
            category.children = get_child_categories(db_category.id, current_level + 1)
            categories.append(category)
        return categories

    if parent_id == 0:
        parent_id = None

    return schemas.CategoryList(categories=get_child_categories(parent_id, 0))

async def get_category_id(db: Session, category_name: str):
    """
    Получает категории из базы данных в соответствии с именем категории.
    """

    db_category = db.query(DBCategory).filter_by(name=category_name).first()

    if not db_category:
        raise HTTPException(status_code=404, detail="Категория не найдена")

    return db_category.id


async def update_catalog(db: Session, category_id: int, category: schemas.ICategoryUpdate):
    """
    Обновляет значения указанной категории в базе данных.
    """
    db_category = db.query(DBCategory).filter_by(id=category_id).first()
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    if category.name:
        db_category.name = category.name
    if category.parent_id is not None:
        parent_id = category.parent_id
        if parent_id == 0:
            parent_id = None
        get_level_nesting(db, parent_id)
        db_category.parent_id = category.parent_id

    db.commit()
    db.refresh(db_category)
    return db_category


async def update_category_sort_order(db: Session, category_id: int, sort: int):
    category = db.query(DBCategory).filter_by(id=category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category.sort = sort
    db.commit()
    db.refresh(category)
    return category

async def delete_catalog(db: Session, category_id: int) -> None:
    """
    Удаляет категорию из базы данных, если она не связана с другими объектами.
    """
    db_category = db.query(DBCategory).filter_by(id=category_id).first()
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        # Проверяем, есть ли дочерние категории
    if db_category.children:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category has child categories")

    db.delete(db_category)
    db.commit()
