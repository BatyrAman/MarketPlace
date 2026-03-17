from uuid import UUID
from fastapi import Depends, Header
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.exceptions import UnauthorizedException, ForbiddenException
from app.core.security import decode_access_token
from app.db.session import get_session
from app.models.user import User, UserRole


async def get_current_user(
    authorization: str | None = Header(default=None),
    session: AsyncSession = Depends(get_session),
) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise UnauthorizedException("Missing bearer token")

    token = authorization.split(" ", 1)[1]

    try:
        payload = decode_access_token(token)
    except ValueError:
        raise UnauthorizedException("Invalid or expired token")

    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedException("Invalid token payload")

    user = await session.get(User, UUID(user_id))
    if not user or not user.is_active:
        raise UnauthorizedException("User not found or inactive")

    return user


def require_roles(*roles: UserRole):
    async def checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise ForbiddenException("You do not have permission for this action")
        return current_user
    return checker
