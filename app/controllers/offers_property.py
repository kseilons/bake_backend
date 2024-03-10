from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.offers import OffersPropertyInfo as DBProp
from app.schemas import offer_property as schemas
from fastapi import HTTPException, status
from app.utils.filter import apply_filters_to_offer_prop
from app.utils.validate import validate_prop_type


async def create_prod_prop(db: Session, prop_create: schemas.OfferPropertyCreate):

    validate_prop_type(prop_create.prop_type)

    db_prop = DBProp(
        name=prop_create.name,
        field_id=prop_create.field_id,
        prop_type=prop_create.prop_type
    )

    db.add(db_prop)
    try:
        db.commit()
    except IntegrityError as e:
        # Обработка ошибки уникальности
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating offer property. {e.orig}"
        )

    db.refresh(db_prop)
    return db_prop

async def get_prod_prop(db: Session, offer_id: int):
    db_catalog = db.query(DBProp).get(offer_id)
    if db_catalog is None:
        raise HTTPException(status_code=404, detail="Offer property not found")
    return db_catalog

async def get_prod_props(db: Session, filters: schemas.OfferPropertyFilter):
    query = db.query(DBProp)
    query = apply_filters_to_offer_prop(query, filters)
    result = query.all()
    return result


async def update_prod_props(db: Session, prop_id: int, prop_update: schemas.OfferPropertyUpdate):
    if (prop_update.prop_type):
        validate_prop_type(prop_update.prop_type)

    try:
        prop = db.query(DBProp).filter(DBProp.id == prop_id).first()
        if prop is None:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Offer property not found")
        update_data = prop_update.model_dump()
        for key, value in update_data.items():
            if value is not None:
                setattr(prop, key, value)

        db.commit()
        db.refresh(prop)

        return prop
    except IntegrityError as e:
        # Обработка ошибки IntegrityError, например, отсутствие внешнего ключа
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,  detail=f"Error updating offer property. {e.orig}")


async def delete_prop(db: Session, prop_id: int):
    prop = db.query(DBProp).filter(DBProp.id == prop_id).first()
    if prop:
        # Удаляем свойство
        db.delete(prop)
        db.commit()
        return {"detail": "offer property deleted successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="offer property not found")


async def insert_prop(db: Session, prop_insert):
    validate_prop_type(prop_insert.prop_type)

    db_prop = db.query(DBProp).filter(DBProp.field_id == prop_insert.field_id).first()

    if db_prop:
        update_data = prop_insert.model_dump()
        for key, value in update_data.items():
            if value is not None:
                setattr(db_prop, key, value)

    else:
        db_prop = DBProp(
            name=prop_insert.name,
            field_id=prop_insert.field_id,
            prop_type=prop_insert.prop_type
        )
        db.add(db_prop)
    try:
        db.commit()
    except IntegrityError as e:
        # Обработка ошибки уникальности
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error insert offer property. {e.orig}"
        )

    db.refresh(db_prop)
    return db_prop
