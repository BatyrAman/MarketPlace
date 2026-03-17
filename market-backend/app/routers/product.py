from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.deps import get_current_user
from app.db.session import get_session
from app.models.user import User
from app.schemas.product import ProductCreate, ProductUpdate, ProductRead
from app.services.product import create_product, list_products, get_product, update_product, delete_product

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product_route(
    data: ProductCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await create_product(session, current_user, data)


@router.get("/", response_model=list[ProductRead])
async def list_products_route(
    search: str | None = Query(default=None),
    category_id: UUID | None = Query(default=None),
    sort_by: str = Query(default="created_at"),
    order: str = Query(default="desc"),
    session: AsyncSession = Depends(get_session),
):
    return await list_products(session, search, category_id, sort_by, order)


@router.get("/{product_id}", response_model=ProductRead)
async def get_product_route(product_id: UUID, session: AsyncSession = Depends(get_session)):
    return await get_product(session, product_id)


@router.patch("/{product_id}", response_model=ProductRead)
async def update_product_route(
    product_id: UUID,
    data: ProductUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await update_product(session, current_user, product_id, data)


@router.delete("/{product_id}")
async def delete_product_route(
    product_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await delete_product(session, current_user, product_id)
    return {"detail": "Product soft-deleted"}
