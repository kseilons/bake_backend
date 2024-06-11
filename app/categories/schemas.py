from typing import List, Optional
from pydantic import BaseModel, Field


class ICategoryCreate(BaseModel):
    name: str = Field(None, description="Имя категории")
    parent_id: Optional[int] = Field(None, description="Родительская категория")
    sort: Optional[int] = Field(0, description="Чем выше значение, тем выше в запросе категория")
    level_nesting: Optional[int] = Field(0, description="Уровень вложенности категории. Задается внутри сервера, в запросе не указывать")

class ICategoryUpdate(BaseModel):
    name: str = Field(None, description="Имя категории")
    parent_id: Optional[int] = Field(0, description="Родительская категория")
    sort: Optional[int] = Field(0, description="Чем выше значение, тем выше в запросе категория")


class ICategoryResponse(BaseModel):
    id: int = Field(None, description="ID категории")
    name: str = Field(None, description="Имя категории")
    level_nesting: int = Field(0, description="Уровень вложенности категории.")
    sort: int = Field(0, description="Чем выше значение, тем выше в запросе категория")
    parent_id: Optional[int] = Field(None, description="ID родительской категории, если такая есть")

class ICategoryWithChildrenResponse(ICategoryResponse):
    children: Optional[list[ICategoryResponse]]

