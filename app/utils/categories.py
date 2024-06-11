from sqlalchemy.orm import Session
from starlette import status

from app.categories.models import Category as DBCategory
from fastapi import HTTPException


# Получаем уровень вложеноости каталога в зависимости от родительского id

def get_level_nesting(db: Session, parent_id):
    if parent_id == 0:
        return 1  # Корневая категория
    parent_catalog = db.query(DBCategory).filter_by(id=parent_id).first()
    if parent_catalog is not None:
        return parent_catalog.level_nesting + 1
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parent category not found")

