from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class IBrandCreate(BaseModel):
    name: str = Field(None, description="Имя бренда")
    
    
class IBrandUpdate(BaseModel):
    name: str = Field(None, description="Имя бренда")
    new_name: str = Field(None, description="Новое имя бренда")

class IBrandResponse(BaseModel):
    id: int = Field(None, description="ID категории")
    name: str = Field(None, description="Имя категории")

    model_config = ConfigDict(from_attributes=True)
