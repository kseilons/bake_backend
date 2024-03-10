from pydantic import BaseModel
from typing import List

from app.schemas.property_info import PropertyInfoList


class ChangeProductInfoCreate(BaseModel):
    catalog_id: int
    prop_ids: List[int]


class ChangeProductInfoUpdate(BaseModel):
    catalog_id: int
    prop_ids: List[int]


class ChangeProductInfo(BaseModel):
    catalog_name: str
    product_info: PropertyInfoList

    class Config:
        from_attributes = True


class ChangeProductInfoList(BaseModel):
    properties: List[ChangeProductInfo]
