from typing import List
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship


class Cart(SQLModel, table=True):
    __tablename__ = "carts"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", unique=True)

    user: "User" = Relationship(back_populates="cart", sa_relationship_kwargs={"lazy": "selectin"})
    items: List["CartItem"] = Relationship(back_populates="cart", sa_relationship_kwargs={"lazy": "selectin"})