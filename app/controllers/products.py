import json
from typing import List

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from app.policy.products import check_correct_product
from app.models.products import Product as DBProduct
from app.models.products import ProductPropertyInfo as DBProductPropertyInfo
from app.models.products import ProductProperty as DBProductProperty
from app.models.catalogs import Catalog as DBCatalog

from app.schemas import products as schemas
from fastapi import HTTPException, status

from app.utils.filter import apply_filters_to_product_query


# TODO Сделать проверку на то, что в property передаются данные соотвествующие ProductPropertyInfo.prop_type
async def create_product(db: Session, product_create: schemas.ProductCreate):
    catalog = db.query(DBCatalog).filter_by(id=product_create.section_id).first()
    if not catalog:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Catalog with id '{product_create.section_id}' does not exist")

    existing_product = db.query(DBProduct).filter_by(old_id=product_create.old_id).first()
    if existing_product:
        db_product = await prod_update(existing_product, product_create, catalog, db)
    else:
        db_product = await prod_create(product_create, catalog, db)

    return schemas.ProductWithProperty.from_db_product(db_product)


async def get_product(db: Session, product_id: int):
    product_info = (
        db.query(DBProduct)
        .options(joinedload(DBProduct.properties).joinedload(DBProductProperty.property_info))
        .filter(DBProduct.id == product_id)
        .first()
    )

    if not product_info:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Product with id '{product_id}' not found")

    return schemas.ProductWithProperty.from_db_product(product_info)


async def get_products_by_ids(db: Session, product_ids: List[int]):
    products_info = (
        db.query(DBProduct)
        .filter(DBProduct.id.in_(product_ids))
        .options(joinedload(DBProduct.properties).joinedload(DBProductProperty.property_info))
        .all()
    )

    if not products_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No products found with the provided IDs")

    return [schemas.ProductWithProperty.from_db_product(product_info) for product_info in products_info]


async def get_products(db: Session, filters: schemas.ProductFilter, page: int, limit: int):
    offset = (page - 1) * limit

    query = db.query(DBProduct)
    query = apply_filters_to_product_query(query, filters)

    result = query.offset(offset).limit(limit).all()
    return result


async def get_product_count_by_order(db: Session, filters: schemas.ProductFilter):
    query = db.query(func.count(DBProduct.id))
    query = apply_filters_to_product_query(query, filters)

    count = query.scalar()
    return count


async def update_product(db: Session, prod_id: int, update_data: schemas.ProductUpdate):
    db_product = db.query(DBProduct).filter_by(id=prod_id).first()
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {prod_id} not found")

    catalog = db.query(DBCatalog).filter_by(id=update_data.section_id).first()

    db_product = await prod_update(db_product, update_data, catalog, db)

    # Возвращаем обновленный продукт
    return schemas.ProductWithProperty.from_db_product(db_product)


#
async def delete_product(db: Session, product_id: int):
    # Получаем информацию о продукте
    product = db.query(DBProduct).filter_by(id=product_id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f"Product with id {product_id} not found")

    db.delete(product)

    db.commit()

    return {
        "detail": "Product deleted successfully"
    }


async def insert_product(db: Session, product_data: schemas.ProductCreate):
    db_product = db.query(DBProduct).filter_by(old_id=product_data.old_id).first()
    catalog = db.query(DBCatalog).filter_by(old_id=product_data.section_id).first()
    if not catalog:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Catalog with old_id '{product_data.section_id}' does not exist")

    if db_product:
        db_product = await prod_update(db_product, product_data, catalog, db)
    else:
        db_product = await prod_create(product_data, catalog, db)
    return schemas.ProductWithProperty.from_db_product(db_product)


async def prop_create(props, product_id, db: Session):
    for field_id, prop_value in props.items():
        prop_info = db.query(DBProductPropertyInfo).filter_by(field_id=field_id).first()
        if not prop_info:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Property Info with field_id '{field_id}' does not exist")

        encoded_value = json.dumps(prop_value, ensure_ascii=False).encode('utf-8')
        db_prop = DBProductProperty(id_product=product_id, id_property_info=prop_info.id, value=encoded_value)
        db.add(db_prop)
        db.commit()
        db.refresh(db_prop)


async def prop_update(props, id_product, db: Session):
    if props is None:
        return

    for field_id, prop_value in props.items():
        prop_info = db.query(DBProductPropertyInfo).filter_by(field_id=field_id).first()
        if not prop_info:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Property Info with field_id '{field_id}' does not exist")

        # Поиск существующего свойства или создание нового
        db_prop = db.query(DBProductProperty).filter_by(id_product=id_product,
                                                        id_property_info=prop_info.id).first()
        if db_prop:
            # Обновление существующего свойства
            db_prop.value = json.dumps(prop_value, ensure_ascii=False).encode('utf-8')
        else:
            # Создание нового свойства
            encoded_value = json.dumps(prop_value, ensure_ascii=False).encode('utf-8')
            db_prop = DBProductProperty(id_product=id_product, id_property_info=prop_info.id, value=encoded_value)
            db.add(db_prop)


async def prod_create(product_data: schemas.ProductCreate, catalog, db: Session):
    await check_correct_product(product_data)  # Проверка полей продукта на корректность
    # Проверка существования каталога

    if not catalog:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Catalog with id '{product_data.section_id}' does not exist")

    db_product = DBProduct(name=product_data.name, section_id=catalog.id,
                           old_id=product_data.old_id, vat=product_data.vat,
                           measure_name=product_data.measure_name, type=product_data.type)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    await prop_create(product_data.properties, db_product.id, db)
    return db_product


async def prod_update(db_product, product_data, new_catalog, db: Session):
    await check_correct_product(product_data)  # Проверка полей продукта на корректность
    if product_data.name:
        db_product.name = product_data.name
    if product_data.section_id:
        if not new_catalog:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Catalog with id '{product_data.section_id}' does not exist")
        db_product.section_id = new_catalog.id
    if product_data.vat:
        db_product.vat = product_data.vat
    if product_data.measure_name:
        db_product.measure_name = product_data.measure_name
    if product_data.type:
        db_product.type = product_data.type
    db.commit()
    db.refresh(db_product)

    await prop_update(product_data.properties, db_product.id, db)
    return db_product
