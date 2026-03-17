from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.deps import get_current_user
from app.db.session import get_session
from app.models.user import User
from app.schemas.user import UserRead

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/me', response_model=UserRead)
async def get_me(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return current_user
