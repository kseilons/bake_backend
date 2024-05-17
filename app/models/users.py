

from sqlalchemy import Integer, String, Column, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .database import Base



class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    phone = Column(String, nullable=True)
    name = Column(String, nullable=True, index=True)
    surname = Column(String, nullable=True)
    patronymic = Column(String, nullable=True)
    hashed_password = Column(String)
    role = Column(String, default='user')
    address = relationship("UsersAddress", uselist=False, back_populates="user")
    tokens = relationship("Token", back_populates="user")
    confirmation_token = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)

class UsersAddress(Base):
    __tablename__ = "users_address"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    region = Column(String)
    city = Column(String)
    street = Column(String)
    num_of_house = Column(String)
    postcode = Column(Integer)

    user = relationship("Users", back_populates="address")

class Token(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(UUID(as_uuid=False), unique=True, nullable=False, index=True)
    expires = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("Users", back_populates="tokens")

