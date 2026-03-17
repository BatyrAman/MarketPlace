from datetime import datetime
from enum import Enum
from typing import Optional, List
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field, Relationship


class UserRole(str, Enum):
    customer = "customer"
    seller = "seller"
    admin = "admin"


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(index=True, unique=True)
    username: str = Field(index=True, unique=True)
    password_hash: str
    full_name: Optional[str] = None
    role: UserRole = Field(default=UserRole.customer)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    products: List["Product"] = Relationship(back_populates="seller", sa_relationship_kwargs={"lazy": "selectin"})
    cart: Optional["Cart"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    orders: List["Order"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    reviews: List["Review"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    refresh_tokens: List["RefreshToken"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})