from decimal import Decimal
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship


class OrderItem(SQLModel, table=True):
    __tablename__ = "order_items"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    order_id: UUID = Field(foreign_key="orders.id")
    product_id: UUID = Field(foreign_key="products.id")
    quantity: int = Field(ge=1)
    price_at_purchase: Decimal = Field(max_digits=10, decimal_places=2)

    order: "Order" = Relationship(back_populates="items", sa_relationship_kwargs={"lazy": "selectin"})
    product: "Product" = Relationship(back_populates="order_items", sa_relationship_kwargs={"lazy": "selectin"})