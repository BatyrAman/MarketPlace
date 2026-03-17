from datetime import datetime, timedelta
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.core.exceptions import ConflictException, UnauthorizedException
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)
from app.models.cart import Cart
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.schemas.auth import RegisterRequest, LoginRequest


async def register_user(session: AsyncSession, data: RegisterRequest):
    existing_email = await session.exec(select(User).where(User.email == data.email))
    if existing_email.first():
        raise ConflictException("Email already registered")

    existing_username = await session.exec(select(User).where(User.username == data.username))
    if existing_username.first():
        raise ConflictException("Username already taken")

    if not isinstance(data.password, str):
        raise ValueError("Password must be string")

    user = User(
        email=data.email,
        username=data.username,
        password_hash=hash_password(data.password),
        full_name=data.full_name,
    )
    session.add(user)
    await session.flush()

    cart = Cart(user_id=user.id)
    session.add(cart)
    await session.commit()
    await session.refresh(user)
    return user


async def login_user(session: AsyncSession, data: LoginRequest):
    result = await session.exec(select(User).where(User.email == data.email))
    user = result.first()
    if not user or not verify_password(data.password, user.password_hash):
        raise UnauthorizedException("Invalid email or password")

    access_token = create_access_token(str(user.id))
    refresh_token = create_refresh_token(str(user.id))

    refresh_token_obj = RefreshToken(
        user_id=user.id,
        token=refresh_token,
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    session.add(refresh_token_obj)
    await session.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


async def refresh_access_token(session: AsyncSession, refresh_token: str):
    try:
        payload = decode_refresh_token(refresh_token)
    except ValueError:
        raise UnauthorizedException("Invalid refresh token")

    token_in_db = await session.exec(select(RefreshToken).where(RefreshToken.token == refresh_token))
    stored = token_in_db.first()
    if not stored:
        raise UnauthorizedException("Refresh token not found")

    user_id = payload.get("sub")
    access_token = create_access_token(user_id)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


async def logout_user(session: AsyncSession, refresh_token: str | None = None):

    if refresh_token:
        result = await session.exec(select(RefreshToken).where(RefreshToken.token == refresh_token))
        token_obj = result.first()
        if token_obj:
            await session.delete(token_obj)
            await session.commit()
