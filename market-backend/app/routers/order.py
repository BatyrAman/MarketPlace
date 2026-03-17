from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.deps import get_current_user
from app.db.session import get_session
from app.models.order import OrderStatus
from app.models.user import User
from app.schemas.order import OrderRead
from app.services.order import create_order_from_cart, list_my_orders, get_order, update_order_status

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/checkout", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def checkout_route(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await create_order_from_cart(session, current_user)


@router.get("/my", response_model=list[OrderRead])
async def list_my_orders_route(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await list_my_orders(session, current_user)


@router.get("/{order_id}", response_model=OrderRead)
async def get_order_route(
    order_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await get_order(session, current_user, order_id)


@router.patch("/{order_id}/status", response_model=OrderRead)
async def update_order_status_route(
    order_id: UUID,
    status: OrderStatus = Query(...),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await update_order_status(session, current_user, order_id, status)
