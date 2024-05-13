from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    level_nesting = Column(Integer)
    parent_id = Column(Integer, ForeignKey('category.id'), nullable=True)
    sort = Column(Integer, default=0)
    parent = relationship("Category", remote_side=[id], back_populates="children")
    children = relationship("Category", back_populates="parent", overlaps="parent")
    products = relationship("Product", back_populates="category")
