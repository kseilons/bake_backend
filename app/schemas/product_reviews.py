from pydantic import BaseModel, Field
from typing import List, Optional

class ReviewsBase(BaseModel):
    user_id: int
    product_id: int
    text: str
    rating: int = Field(..., ge=0, le=5)

class ReviewCreate(ReviewsBase):
    pass

class ReviewUpdate(BaseModel):
    text: Optional[str] = None
    rating: Optional[float] = None

class Review(ReviewsBase):
    id: int

    class Config:
        orm_mode = True

class ReviewList(BaseModel):
    reviews: List[Review]

    class Config:
        orm_mode = True
