from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship


class OrderStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    cancelled = "cancelled"
    delivered = "delivered"


class Order(SQLModel, table=True):
    __tablename__ = "orders"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    total_amount: Decimal = Field(default=0, max_digits=12, decimal_places=2)
    status: OrderStatus = Field(default=OrderStatus.pending)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: "User" = Relationship(back_populates="orders", sa_relationship_kwargs={"lazy": "selectin"})
    items: List["OrderItem"] = Relationship(back_populates="order", sa_relationship_kwargs={"lazy": "selectin"})