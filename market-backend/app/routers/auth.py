from fastapi import APIRouter, Depends, Header
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import get_session
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.schemas.user import UserRead
from app.services.auth import register_user, login_user, refresh_access_token, logout_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserRead)
async def register(data: RegisterRequest, session: AsyncSession = Depends(get_session)):
    return await register_user(session, data)


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, session: AsyncSession = Depends(get_session)):
    return await login_user(session, data)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(refresh_token: str, session: AsyncSession = Depends(get_session)):
    return await refresh_access_token(session, refresh_token)


@router.post("/logout")
async def logout(
    refresh_token: str | None = None,
    authorization: str | None = Header(default=None),
    session: AsyncSession = Depends(get_session),
):
    access_token = authorization.split(" ", 1)[1] if authorization else ""
    await logout_user(session, access_token, refresh_token)
    return {"detail": "Logged out successfully"}
