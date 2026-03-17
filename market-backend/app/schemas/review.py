from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    product_id: UUID
    rating: int = Field(ge=1, le=5)
    comment: str | None = None


class ReviewUpdate(BaseModel):
    rating: int | None = Field(default=None, ge=1, le=5)
    comment: str | None = None


class ReviewRead(BaseModel):
    id: UUID
    user_id: UUID
    product_id: UUID
    rating: int
    comment: str | None
    created_at: datetime