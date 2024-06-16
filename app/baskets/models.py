from typing import List
import uuid
import datetime

from sqlalchemy import UUID, Integer, String, Column, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped, mapped_column

from ..db.session import Base


class Basket(Base):
    __tablename__ = "basket"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"))
    updated_date: Mapped[datetime.datetime] = mapped_column(default=datetime.UTC)

    items: Mapped[List["BasketItem"]] = relationship(
        back_populates="basket", cascade="all, delete-orphan"
    )


class BasketItem(Base):
    __tablename__ = "basket_item"
    id: Mapped[int] = mapped_column(primary_key=True)
    basket_id: Mapped[int] = mapped_column(ForeignKey("basket.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))
    amount: Mapped[int] = mapped_column()

    basket: Mapped["Basket"] = relationship(back_populates="items")
    product:  Mapped["Product"] = relationship()