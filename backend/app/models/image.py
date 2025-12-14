from typing import Optional
import uuid
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from app.database import Base

class Image(Base):
    __tablename__ = "images"
    
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    s3_key: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    product_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)