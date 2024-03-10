from .database import Base

from sqlalchemy import Column, ForeignKey, Integer, String, Float, Text
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    preview_img = Column(String)  # URL для предварительного изображения
    rating_avg = Column(Float) # Пересчитывается при добавлении/редактировании отзыва для продукта
    category_id = Column(Integer, ForeignKey('category.id'))
    short_description = Column(String)
    sort = Column(Integer)

    info = relationship("ProductInfo", back_populates="product")  # Обратная связь с ProductInfo
    images = relationship("ProductImage", back_populates="product")
    reviews = relationship("ProductRating", back_populates="product")


class ProductImage(Base):
    __tablename__ = "product_images"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    url = Column(String)  # URL изображения

    product = relationship("Product", back_populates="images")


class ProductInfo(Base):
    __tablename__ = "product_info"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text)
    product_id = Column(Integer, ForeignKey('products.id'))

    properties = relationship("ProductProperty", back_populates="product_info")


class ProductReview(Base):
    __tablename__ = "product_reviews"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    text = Column(Text)
    rating = Column(Integer)

    product = relationship("Product", back_populates="reviews")

