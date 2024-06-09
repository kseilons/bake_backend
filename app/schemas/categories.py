from typing import List, Optional
from pydantic import BaseModel


class ICategoryCreate(BaseModel):
    name: str
    parent_id: Optional[int] = 0
    sort: Optional[int] = 0

class ICategoryUpdate(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[int] = None


class CategoryChangeResponse(BaseModel):
    id: int
    name: str
    level_nesting: int
    sort: int
    parent_id: Optional[int]
    class Config:
        from_attributes = True



class Category(BaseModel):
    id: int
    name: str
    level_nesting: int
    sort: int
    children: List['Category'] = []

    class Config:
        from_attributes = True

class CategoryList(BaseModel):
    categories: List[Category] = []
