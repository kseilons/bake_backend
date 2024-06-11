from typing import List
from sqlalchemy import  String
from sqlalchemy.orm import Mapped, mapped_column

from fastapi_users.db import SQLAlchemyBaseUserTableUUID


from app.db.session import Base

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"
    region: Mapped[str] = mapped_column(String(50), nullable=True)
    city: Mapped[str] = mapped_column(String(50), nullable=True)
    street: Mapped[str] = mapped_column(String(50), nullable=True)
    num_of_house: Mapped[str] = mapped_column(String(50), nullable=True)
    postcode: Mapped[int] = mapped_column(nullable=True)
    phone: Mapped[str] = mapped_column(String(55), nullable=True)
    name:  Mapped[str] = mapped_column(String(55), nullable=True)
    surname:  Mapped[str] = mapped_column(String(50), nullable=True)
    patronymic: Mapped[str] = mapped_column(String(50), nullable=True)


