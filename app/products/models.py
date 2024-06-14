import datetime
from typing import List

from app.categories.models import Category

from ..db.session import Base

from sqlalchemy import Column, Date, ForeignKey, Integer, String, Float, Text, Boolean, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy_file import FileField, ImageField


class Product(Base):
    __tablename__ = "product"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    create_date: Mapped[datetime.datetime] = mapped_column(default=func.now())
    title: Mapped[str] = mapped_column(unique=True)
    preview_img: Mapped[str]
    # rating_avg: Mapped[float]
    # rating_count: Mapped[int]
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    sort: Mapped[int]
    price: Mapped[int]
    old_price: Mapped[int]
    is_hit: Mapped[bool]
    brand: Mapped[str]
    description: Mapped[str]
    article: Mapped[str]
    
    category: Mapped["Category"] = relationship()
    properties: Mapped[List["ProductProperty"]] = relationship(back_populates="product", cascade="all, delete")
    images: Mapped[List["ProductImage"]] = relationship(back_populates="product", cascade="all, delete")
    files: Mapped[List["ProductFile"]] = relationship( back_populates="product", cascade="all, delete")
    # reviews: Mapped[List["ProductReview"]] = relationship(ack_populates="product", cascade="all, delete")


class ProductImage(Base):
    __tablename__ = "product_image"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    image_url: Mapped[str] = mapped_column(String)
    alt: Mapped[str] = mapped_column(String)
    product: Mapped["Product"] = relationship(back_populates="images")


class ProductProperty(Base):
    __tablename__ = "product_property"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    prod_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    value: Mapped[str]
    name: Mapped[str]
    product: Mapped["Product"] = relationship(back_populates="properties")


class ProductFile(Base):
    __tablename__ = "product_files"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
    file: Mapped[str]

    product: Mapped["Product"] = relationship(back_populates="files")



# class ProductReview(Base):
#     __tablename__ = "product_reviews"
#     id: Mapped[int] = mapped_column(primary_key=True, index=True)
#     product_id: Mapped[int] = mapped_column(ForeignKey('product.id'))
#     user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
#     text: Mapped[str]
#     rating: Mapped[int]

#     product: Mapped["Product"] = relationship(back_populates="reviews")