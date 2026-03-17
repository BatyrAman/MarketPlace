from datetime import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel
from app.models.order import OrderStatus


class OrderItemRead(BaseModel):
    id: UUID
    product_id: UUID
    quantity: int
    price_at_purchase: Decimal


class OrderRead(BaseModel):
    id: UUID
    user_id: UUID
    total_amount: Decimal
    status: OrderStatus
    created_at: datetime
    items: list[OrderItemRead]
