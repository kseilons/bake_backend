
from app.models.categories import Category
from app.models.product_properties import PropertyInfo, ChangeProduct
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas import props_for_product as schemas
from app.schemas.property_info import PropertyInfoList
from app.schemas.props_for_product import ChangeProductInfo
def get_schem_by_catalog_id(catalog_id: int, db: Session):
    """
    Получает схему свойств продукта для указанной категории.
    """
    # Проверяем существование категории
    category = db.query(Category).filter_by(id=catalog_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Получаем все свойства для указанной категории
    schem_properties = db.query(ChangeProduct).filter_by(category_id=catalog_id).all()

    # Создаем список объектов схемы продукта для ответа
    product_schems = []
    for schem in schem_properties:
        prop = db.query(PropertyInfo).filter_by(id=schem.property_id).first()
        if prop:
            product_schems.append(PropertyInfo(id=prop.id, name=prop.name, measurement=prop.measurement))

    # Создаем экземпляр PropertyInfoList
    product_info_list = PropertyInfoList(properties=product_schems)

    # Создаем экземпляр ChangeProductInfo
    change_product_info = ChangeProductInfo(catalog_name=category.name, product_info=product_info_list)

    return change_product_info



def create_new_schem(schem_info: schemas.ChangeProductInfoCreate, db: Session):
    """
    Создает схему свойств продукта для указанной категории.
    """
    category = db.query(Category).filter_by(id=schem_info.catalog_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    schem_properties = []
    for prop_id in schem_info.prop_ids:
        prop = db.query(PropertyInfo).filter_by(id=prop_id).first()
        if not prop:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Property with ID {prop_id} not found")

        existing_schem = db.query(ChangeProduct).filter_by(category_id=category.id, property_id=prop_id).first()
        if existing_schem:
            continue

        db_schem_prop = ChangeProduct(category_id=category.id, property_id=prop_id)
        db.add(db_schem_prop)
        schem_properties.append(prop)
        db.commit()
        db.refresh(db_schem_prop)

    product_schems = []
    for prop in schem_properties:
        product_schems.append(PropertyInfo(id=prop.id, name=prop.name, measurement=prop.measurement))

    product_info_list = PropertyInfoList(properties=product_schems)
    change_product_info = ChangeProductInfo(catalog_name=category.name, product_info=product_info_list)

    return change_product_info

def update_schem(schem_info: schemas.ChangeProductInfoUpdate, db: Session):
    """
    Обновляет схему свойств продукта для указанной категории.
    """
    category = db.query(Category).filter_by(id=schem_info.catalog_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    db.query(ChangeProduct).filter_by(category_id=schem_info.catalog_id). \
        filter(~ChangeProduct.property_id.in_(schem_info.prop_ids)).delete(synchronize_session=False)

    existing_schems = set()
    for prop_id in schem_info.prop_ids:
        existing_schem = db.query(ChangeProduct).filter_by(category_id=schem_info.catalog_id,
                                                           property_id=prop_id).first()
        if existing_schem:
            continue

        db_schem_prop = ChangeProduct(category_id=schem_info.catalog_id, property_id=prop_id)
        db.add(db_schem_prop)
        existing_schems.add((schem_info.catalog_id, prop_id))

    db.commit()

    product_schems = []
    for category_id, prop_id in existing_schems:
        prop = db.query(PropertyInfo).filter_by(id=prop_id).first()
        product_schems.append(PropertyInfo(id=prop.id, name=prop.name, measurement=prop.measurement))

    product_info_list = PropertyInfoList(properties=product_schems)
    change_product_info = ChangeProductInfo(catalog_name=category.name, product_info=product_info_list)

    return change_product_info