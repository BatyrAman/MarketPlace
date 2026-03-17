from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.deps import get_current_user
from app.db.session import get_session
from app.models.user import User
from app.schemas.cart import CartRead, CartItemCreate, CartItemUpdate, CartItemRead
from app.services.cart import get_my_cart, add_to_cart, update_cart_item, remove_cart_item

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("/", response_model=CartRead)
async def get_cart_route(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await get_my_cart(session, current_user)


@router.post("/items", response_model=CartItemRead, status_code=status.HTTP_201_CREATED)
async def add_to_cart_route(
    data: CartItemCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await add_to_cart(session, current_user, data)


@router.patch("/items/{item_id}", response_model=CartItemRead)
async def update_cart_item_route(
    item_id: UUID,
    data: CartItemUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await update_cart_item(session, current_user, item_id, data)


@router.delete("/items/{item_id}")
async def remove_cart_item_route(
    item_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await remove_cart_item(session, current_user, item_id)
    return {"detail": "Item removed from cart"}
