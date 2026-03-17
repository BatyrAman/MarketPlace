from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: Decimal = Field(gt=0)
    stock: int = Field(ge=0)
    category_id: UUID


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: Decimal | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)
    is_active: bool | None = None
    category_id: UUID | None = None


class ProductRead(BaseModel):
    id: UUID
    name: str
    description: str | None
    price: Decimal
    stock: int
    is_active: bool
    seller_id: UUID
    category_id: UUID
    created_at: datetime
