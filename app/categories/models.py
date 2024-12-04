from sqlalchemy import  Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column


from ..db.session import Base

    
category_brand = Table(
    'category_brand', Base.metadata,
    Column('category_id', Integer, ForeignKey('category.id'), primary_key=True),
    Column('brand_id', Integer, ForeignKey('brand.id'), primary_key=True)
)


class Category(Base):
    __tablename__ = "category"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    level_nesting: Mapped[int] = mapped_column(nullable=True)
    parent_id:  Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=True)
    sort: Mapped[int] = mapped_column(default=0)
    parent: Mapped["Category"] = relationship(
        "Category", 
        remote_side=[id], 
        back_populates="children", 
        uselist=False,
    )
    children: Mapped[list["Category"]] = relationship(
        "Category", 
        back_populates="parent", 
        overlaps="parent",
        cascade="all, delete-orphan"
    )

    brands: Mapped[list["Brand"]] = relationship(
        "Brand",
        secondary=category_brand,
        back_populates="categories"
    )


class Brand(Base):
    __tablename__ = "brand"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True)
    
    categories: Mapped[list["Category"]] = relationship(
        "Category",
        secondary=category_brand,
        back_populates="brands"
    )