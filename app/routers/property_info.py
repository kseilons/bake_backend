from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import property_info as schemas
from app.models.database import get_db
from app.models.product_properties import PropertyInfo

router = APIRouter(tags=["property_info"])


@router.post("/", response_model=schemas.PropertyInfo)
async def create_property_info(property_info: schemas.PropertyInfoCreate, db: Session = Depends(get_db)):
    """
    Создает новую информацию о свойстве.
    """
    db_property_info = PropertyInfo(**property_info.dict())
    db.add(db_property_info)
    db.commit()
    db.refresh(db_property_info)
    return db_property_info


@router.get("/", response_model=schemas.PropertyInfoList)
async def get_all_property_info(db: Session = Depends(get_db)):
    """
    Возвращает список всех информаций о свойствах.
    """
    properties = db.query(PropertyInfo).all()
    property_info_list = []
    for property_info in properties:
        property_dict = {
            "id": property_info.id,
            "name": property_info.name,
            "measurement": property_info.measurement
        }
        property_info_list.append(property_dict)
    return schemas.PropertyInfoList(properties=property_info_list)


@router.delete("/{property_info_id}/")
async def delete_property_info(property_info_id: int, db: Session = Depends(get_db)):
    """
    Удаляет информацию о свойстве по ее идентификатору.
    """
    property_info = db.query(PropertyInfo).filter_by(id=property_info_id).first()
    if not property_info:
        raise HTTPException(status_code=404, detail="Property info not found")
    db.delete(property_info)
    db.commit()
    return {"message": "Property info deleted successfully"}


@router.put("/{property_info_id}/", response_model=schemas.PropertyInfo)
async def update_property_info(property_info_id: int, property_info_update: schemas.PropertyInfoUpdate,
                               db: Session = Depends(get_db)):
    """
    Обновляет информацию о свойстве по ее идентификатору.
    """
    db_property_info = db.query(PropertyInfo).filter_by(id=property_info_id).first()
    if not db_property_info:
        raise HTTPException(status_code=404, detail="Property info not found")

    # Обновляем свойства информации о свойстве
    for field, value in property_info_update.dict(exclude_unset=True).items():
        setattr(db_property_info, field, value)

    db.commit()
    db.refresh(db_property_info)
    return db_property_info
