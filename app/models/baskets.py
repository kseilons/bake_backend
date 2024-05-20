from sqlalchemy import Integer, String, Column, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .database import Base


class Basket(Base):
    __tablename__ = "basket"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    updated_date = Column(DateTime, default=func.now())

    items = relationship("BasketItem", back_populates="basket", cascade="all, delete-orphan")


class BasketItem(Base):
    __tablename__ = "basket_items"
    id = Column(Integer, primary_key=True, index=True)
    basket_id = Column(Integer, ForeignKey('basket.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    amount = Column(Integer)

    basket = relationship("Basket", back_populates="items")
    product = relationship("Product")
