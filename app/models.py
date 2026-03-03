from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.database import Base


# ── SQLAlchemy ORM Model (DB table) ──────────────────────────────

class ItemModel(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), default="")
    price = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ── Pydantic Schemas (request/response) ─────────────────────────

class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(default="", max_length=500)
    price: float = Field(..., gt=0)


class ItemUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    price: Optional[float] = Field(default=None, gt=0)


class ItemResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    created_at: datetime

    class Config:
        from_attributes = True
