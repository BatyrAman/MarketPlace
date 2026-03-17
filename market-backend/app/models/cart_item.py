from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship


class CartItem(SQLModel, table=True):
    __tablename__ = "cart_items"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    cart_id: UUID = Field(foreign_key="carts.id")
    product_id: UUID = Field(foreign_key="products.id")
    quantity: int = Field(default=1, ge=1)

    cart: "Cart" = Relationship(back_populates="items", sa_relationship_kwargs={"lazy": "selectin"})
    product: "Product" = Relationship(back_populates="cart_items", sa_relationship_kwargs={"lazy": "selectin"})