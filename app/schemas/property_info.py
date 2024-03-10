from pydantic import BaseModel
from typing import Optional, List


class PropertyInfoCreate(BaseModel):
    name: str
    measurement: Optional[str] = None


class PropertyInfoUpdate(BaseModel):
    name: Optional[str] = None
    measurement: Optional[str] = None


class PropertyInfo(BaseModel):
    id: int
    name: str
    measurement: Optional[str] = None

    class Config:
        from_attributes = True


class PropertyInfoList(BaseModel):
    properties: List[PropertyInfo] = []
