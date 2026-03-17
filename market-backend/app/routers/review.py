from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.deps import get_current_user
from app.db.session import get_session
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewRead
from app.services.review import create_review, list_product_reviews, update_review, delete_review

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("/", response_model=ReviewRead, status_code=status.HTTP_201_CREATED)
async def create_review_route(
    data: ReviewCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await create_review(session, current_user, data)


@router.get("/product/{product_id}", response_model=list[ReviewRead])
async def list_product_reviews_route(product_id: UUID, session: AsyncSession = Depends(get_session)):
    return await list_product_reviews(session, product_id)


@router.patch("/{review_id}", response_model=ReviewRead)
async def update_review_route(
    review_id: UUID,
    data: ReviewUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return await update_review(session, current_user, review_id, data)


@router.delete("/{review_id}")
async def delete_review_route(
    review_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    await delete_review(session, current_user, review_id)
    return {"detail": "Review deleted"}
