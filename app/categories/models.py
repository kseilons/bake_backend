from sqlalchemy import  String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.models.products import Product

from ..db.session import Base


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
    products: Mapped[list["Product"]] = relationship(
        "Product", 
        back_populates="category",
        cascade="all, delete-orphan"
    )