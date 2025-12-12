from typing import Optional
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from app.database import Base
from app.models.parish import Parish
from enum import Enum

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=True)
    parish: Mapped[Optional[Parish]] = mapped_column(String, default=None, nullable=True)
    admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

