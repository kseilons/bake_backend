from .database import Base

from sqlalchemy import Column, ForeignKey, Integer, String, Float, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy_file import FileField, ImageField


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    preview_img = Column(String)
    rating_avg = Column(Float)  # Пересчитывается при добавлении/редактировании отзыва для продукта
    rating_count = Column(Integer)
    category_id = Column(Integer, ForeignKey('category.id'))
    short_description = Column(String)
    sort = Column(Integer)
    price = Column(Integer)
    old_price = Column(Integer)
    is_hit = Column(Boolean)
    brand = Column(String)
    category = relationship("Category", back_populates="products")
    info = relationship("ProductInfo", back_populates="product", cascade="all, delete")
    properties = relationship("ProductProperty", back_populates="product", cascade="all, delete")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete")
    files = relationship("ProductFile", back_populates="product", cascade="all, delete")
    reviews = relationship("ProductReview", back_populates="product")

class ProductImage(Base):
    __tablename__ = "product_images"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    image_url = Column(String)
    alt = Column(String)

    product = relationship("Product", back_populates="images")


class ProductProperty(Base):
    __tablename__ = "product_property"
    id = Column(Integer, primary_key=True, index=True)
    prod_id = Column(Integer, ForeignKey('products.id'))
    value = Column(String)
    name = Column(String)

    product = relationship("Product", back_populates="properties")


class ProductFile(Base):
    __tablename__ = "product_files"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    file = Column(String)

    product = relationship("Product", back_populates="files")


class ProductInfo(Base):
    __tablename__ = "product_info"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text)
    product_id = Column(Integer, ForeignKey('products.id'))
    article = Column(Integer)
    product = relationship("Product", back_populates="info")

class ProductReview(Base):
    __tablename__ = "product_reviews"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    text = Column(Text)
    rating = Column(Integer)

    product = relationship("Product", back_populates="reviews")
