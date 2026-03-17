from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field


class CartItemCreate(BaseModel):
    product_id: UUID
    quantity: int = Field(ge=1)


class CartItemUpdate(BaseModel):
    quantity: int = Field(ge=1)


class CartItemRead(BaseModel):
    id: UUID
    product_id: UUID
    quantity: int


class CartRead(BaseModel):
    id: UUID
    user_id: UUID
    items: list[CartItemRead]
