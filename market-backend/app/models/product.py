from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship


class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    price: Decimal = Field(max_digits=10, decimal_places=2)
    stock: int = Field(default=0, ge=0)
    is_active: bool = Field(default=True)
    seller_id: UUID = Field(foreign_key="users.id", index=True)
    category_id: UUID = Field(foreign_key="categories.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    seller: "User" = Relationship(back_populates="products", sa_relationship_kwargs={"lazy": "selectin"})
    category: "Category" = Relationship(back_populates="products", sa_relationship_kwargs={"lazy": "selectin"})
    reviews: List["Review"] = Relationship(back_populates="product", sa_relationship_kwargs={"lazy": "selectin"})
    order_items: List["OrderItem"] = Relationship(back_populates="product", sa_relationship_kwargs={"lazy": "selectin"})
    cart_items: List["CartItem"] = Relationship(back_populates="product", sa_relationship_kwargs={"lazy": "selectin"})