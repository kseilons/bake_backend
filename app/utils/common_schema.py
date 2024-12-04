
from enum import Enum

from pydantic import BaseModel


class IOrderEnum(str, Enum):
    asc = "asc"
    des = "descendent"
    
class PaginationList(BaseModel):
    total_pages: int
    total_count: int