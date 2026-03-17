from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.deps import require_roles
from app.db.session import get_session
from app.models.user import User, UserRole
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryRead
from app.services.category import create_category, list_categories, update_category, delete_category

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category_route(
    data: CategoryCreate,
    session: AsyncSession = Depends(get_session),
    _: User = Depends(require_roles(UserRole.admin)),
):
    return await create_category(session, data)


@router.get("/", response_model=list[CategoryRead])
async def list_categories_route(session: AsyncSession = Depends(get_session)):
    return await list_categories(session)


@router.patch("/{category_id}", response_model=CategoryRead)
async def update_category_route(
    category_id: str,
    data: CategoryUpdate,
    session: AsyncSession = Depends(get_session),
):
    return await update_category(session, category_id, data)


@router.delete("/{category_id}")
async def delete_category_route(
    category_id: str,
    session: AsyncSession = Depends(get_session),
    _: User = Depends(require_roles(UserRole.admin)),
):
    await delete_category(session, category_id)
    return {"detail": "Category deleted"}
