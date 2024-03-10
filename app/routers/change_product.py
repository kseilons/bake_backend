from app.controllers import change_product as controllers
from app.models.categories import Category
from app.models.product_properties import PropertyInfo, ChangeProduct
from app.models.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.schemas import props_for_product as schemas
from app.schemas.property_info import PropertyInfoList
from app.schemas.props_for_product import ChangeProductInfo
from app.schemas.users import User
from app.utils.dependecies import verify_admin_user

router = APIRouter(tags=['schem_product'])


@router.post("/", response_model=schemas.ChangeProductInfo, status_code=status.HTTP_201_CREATED)
async def create_new_schem(schem_info: schemas.ChangeProductInfoCreate, db: Session = Depends(get_db),
                           current_user: User = Depends(verify_admin_user)):
    """
    Устанавливает схему свойств продукта для указанной категории.
    """
    return controllers.create_new_schem(schem_info, db)


@router.put("/", response_model=schemas.ChangeProductInfo, status_code=status.HTTP_200_OK)
async def update_schem(schem_info: schemas.ChangeProductInfoUpdate, db: Session = Depends(get_db),
                       current_user: User = Depends(verify_admin_user)):
    """
    Обновляет схему свойств продукта для указанной категории.
    """
    return controllers.update_schem(schem_info, db)


@router.get("/{catalog_id}", response_model=schemas.ChangeProductInfo, status_code=status.HTTP_200_OK)
async def get_schem_by_catalog_id(catalog_id: int, db: Session = Depends(get_db)):
    """
    Возвращает схему свойств продукта для указанной категории.
    """
    return controllers.get_schem_by_catalog_id(catalog_id, db)
