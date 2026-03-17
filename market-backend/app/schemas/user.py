from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr
from app.models.user import UserRole


class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    username: str
    full_name: str | None
    role: UserRole
    is_active: bool
    created_at: datetime


class UserUpdateRole(BaseModel):
    role: UserRole
