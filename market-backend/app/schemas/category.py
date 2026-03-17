from uuid import UUID
from pydantic import BaseModel

class CategoryCreate(BaseModel):
    category_id: UUID
    name: str
    description: str | None = None


class CategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class CategoryRead(BaseModel):
    id: UUID
    name: str
    description: str | None
