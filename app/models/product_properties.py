from .database import Base

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class ProductProperty(Base):
    __tablename__ = "product_property"
    id = Column(Integer, primary_key=True, index=True)
    prop_id = Column(Integer)
    value = Column(String)
    property_info_id = Column(Integer, ForeignKey('property_info.id'))

    property_info = relationship("PropertyInfo")

class PropertyInfo(Base):
    __tablename__ = "property_info"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    measurement = Column(String, nullable=True)

    properties = relationship("ProductProperty", back_populates="property_info")

class ChangeProduct(Base):
    __tablename__ = "change_product"
    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, ForeignKey('property_info.id'))
    category_id = Column(Integer, ForeignKey('category.id'))
