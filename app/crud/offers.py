import json
from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from app.models.products import Product as DBProduct
from app.models.offers import Offers as DBOffers
from app.models.offers import OffersProperty as DBOffersProperty
from app.models.offers import OffersPropertyInfo as DBOffersPropertyInfo
from app.policy.offers import check_correct_offer
from app.schemas import offers as schemas
from fastapi import HTTPException, status

from app.utils.filter import apply_filters_to_offer_query


# TODO Сделать проверку на то, что в property передаются данные соотвествующие ProductPropertyInfo.prop_type
async def create_offer(db: Session, offers_create: schemas.OffersCreate):
    # Проверка существования продукта
    product = db.query(DBProduct).filter_by(id=offers_create.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Product with id '{offers_create.product_id}' does not exist")

    db_offers = crud_offer_create(db, offers_create, product)

    return schemas.OfferWithProperty.from_db_offer(db_offers)


async def get_offer(db: Session, offer_id: int):
    offer_info = (
        db.query(DBOffers)
        .options(joinedload(DBOffers.properties).joinedload(DBOffersProperty.property_info))
        .filter(DBOffers.id == offer_id)
        .first()
    )

    if not offer_info:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Offer with id '{offer_id}' not found")

    return schemas.OfferWithProperty.from_db_offer(offer_info)


async def get_offers(db: Session, filters: schemas.OffersFilter, page: int, limit: int):
    offset = (page - 1) * limit
    query = db.query(DBOffers)
    query = apply_filters_to_offer_query(query, filters)

    result = query.offset(offset).limit(limit).all()
    return result


async def get_offers_by_ids(db: Session, offers_ids: List[int]):
    offers_info = (
        db.query(DBOffers)
        .filter(DBOffers.id.in_(offers_ids))
        .options(joinedload(DBOffers.properties).joinedload(DBOffersProperty.property_info))
        .all()
    )

    if not offers_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No offers found with the provided IDs")

    return [schemas.OfferWithProperty.from_db_offer(offer_info) for offer_info in offers_info]


async def get_offers_count(db: Session, filters: schemas.OffersFilter):
    query = db.query(func.count(DBOffers.id))
    query = apply_filters_to_offer_query(query, filters)

    count = query.scalar()
    return count


async def update_offer(db: Session, offer_id: int, offer_data: schemas.OffersUpdate):
    offer = db.query(DBOffers).filter_by(id=offer_id).first()
    if not offer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Offer with id {offer_id} not found")

    if offer_data.product_id:
        # Проверка существования нового товара
        product = db.query(DBProduct).filter_by(id=offer_data.product_id).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Product with id '{offer_data.product_id}' does not exist")
    else:
        product = db.query(DBProduct).filter_by(id=offer.product_id).first()
    offer = await crud_offer_update(db, offer_data, offer, product)

    # Возвращаем обновленный продукт
    return schemas.OfferWithProperty.from_db_offer(offer)


#
async def delete_offer(db: Session, id_offer: int):
    # Получаем информацию о продукте
    offer = db.query(DBOffers).filter_by(id=id_offer).first()

    if not offer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Offer with id {id_offer} not found")

    # Удаляем свойства продукта
    db.query(DBOffersProperty).filter_by(id_offer=id_offer).delete()

    # Удаляем сам продукт
    db.query(DBOffers).filter_by(id=id_offer).delete()

    db.commit()
    return {"detail": f"Offer with id {id_offer} has been deleted successfully"}


async def insert_offer(db: Session, offer_data: schemas.OffersCreate):
    # Проверка существования продукта
    product = db.query(DBProduct).filter_by(old_id=offer_data.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Product with old_id '{offer_data.product_id}' does not exist")

    offer = db.query(DBOffers).filter_by(old_id=offer_data.old_id).first()
    if offer:
        offer = await crud_offer_update(db, offer_data, offer, product)
    else:
        offer = await crud_offer_create(db, offer_data, product)

    return schemas.OfferWithProperty.from_db_offer(offer)


async def prop_create(db, prop_data, offer_id):
    for field_id, prop_value in prop_data:
        prop_info = db.query(DBOffersPropertyInfo).filter_by(field_id=field_id).first()
        if not prop_info:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Property Info with field_id '{field_id}' does not exist")

        encoded_value = json.dumps(prop_value, ensure_ascii=False).encode('utf-8')
        db_prop = DBOffersProperty(id_offer=offer_id, id_property_info=prop_info.id, value=encoded_value)
        db.add(db_prop)
        db.commit()
        db.refresh(db_prop)


async def prop_update(db, props, offer_id):
    # Обновление свойств торгового предложения
    for field_id, prop_value in props:
        prop_info = db.query(DBOffersPropertyInfo).filter_by(field_id=field_id).first()
        if not prop_info:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Property Info with field_id '{field_id}' does not exist")

        # Поиск существующего свойства или создание нового
        db_prop = db.query(DBOffersProperty).filter_by(id_offer=offer_id,
                                                       id_property_info=prop_info.id).first()
        if db_prop:
            # Обновление существующего свойства
            db_prop.value = json.dumps(prop_value, ensure_ascii=False).encode('utf-8')
        else:
            # Создание нового свойства
            encoded_value = json.dumps(prop_value, ensure_ascii=False).encode('utf-8')
            db_prop = DBOffersProperty(id_offer=offer_id, id_property_info=prop_info.id, value=encoded_value)
            db.add(db_prop)


async def crud_offer_create(db, offer_data, product):
    offer_data = await pull_values_from_product(offer_data, product)
    await check_correct_offer(offer_data)  # Проверка полей продукта на корректность

    offer = DBOffers(name=offer_data.name, product_id=product.id, old_id=offer_data.old_id,
                     vat=offer_data.vat, measure_name=offer_data.measure_name, type=offer_data.type)
    db.add(offer)
    db.commit()
    db.refresh(offer)
    await prop_create(db, offer_data.properties.items(), offer.id)
    return offer


async def crud_offer_update(db, offer_data, offer, product):
    await check_correct_offer(offer_data)  # Проверка полей предложения на корректность
    if offer_data.name:
        offer.name = offer_data.name
    if product.id:
        offer.product_id = product.id
    if offer_data.vat:
        offer.vat = offer_data.vat
    if offer_data.measure_name:
        offer.measure_name = offer_data.measure_name
    if offer_data.type:
        offer.type = offer_data.type

    db.commit()
    db.refresh(offer)
    await prop_update(db, offer_data.properties.items(), offer.id)
    return offer


async def pull_values_from_product(offer_data, product):
    if not offer_data.vat:
        offer_data.vat = product.vat
    if not offer_data.measure_name:
        offer_data.measure_name = product.measure_name
    if not offer_data.type:
        offer_data.type = product.type
    return offer_data
