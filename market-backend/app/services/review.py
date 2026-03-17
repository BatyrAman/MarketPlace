from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.exceptions import ConflictException, ForbiddenException, NotFoundException
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.review import Review
from app.models.user import User, UserRole
from app.schemas.review import ReviewCreate, ReviewUpdate


async def create_review(session: AsyncSession, current_user: User, data: ReviewCreate):
    product = await session.get(Product, data.product_id)
    if not product or not product.is_active:
        raise NotFoundException("Product not found")

    order_check = await session.exec(
        select(OrderItem)
        .join(Order, Order.id == OrderItem.order_id)
        .where(Order.user_id == current_user.id, OrderItem.product_id == data.product_id)
    )
    purchased = order_check.first()
    if not purchased:
        raise ForbiddenException("You can review only purchased products")

    existing = await session.exec(
        select(Review).where(Review.user_id == current_user.id, Review.product_id == data.product_id)
    )
    if existing.first():
        raise ConflictException("You already reviewed this product")

    review = Review(user_id=current_user.id, **data.model_dump())
    session.add(review)
    await session.commit()
    await session.refresh(review)
    return review


async def list_product_reviews(session: AsyncSession, product_id):
    result = await session.exec(select(Review).where(Review.product_id == product_id).order_by(Review.created_at.desc()))
    return result.all()


async def update_review(session: AsyncSession, current_user: User, review_id, data: ReviewUpdate):
    review = await session.get(Review, review_id)
    if not review:
        raise NotFoundException("Review not found")

    if current_user.role != UserRole.admin and review.user_id != current_user.id:
        raise ForbiddenException("You can update only your own review")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(review, key, value)

    session.add(review)
    await session.commit()
    await session.refresh(review)
    return review


async def delete_review(session: AsyncSession, current_user: User, review_id):
    review = await session.get(Review, review_id)
    if not review:
        raise NotFoundException("Review not found")

    if current_user.role != UserRole.admin and review.user_id != current_user.id:
        raise ForbiddenException("You can delete only your own review")

    await session.delete(review)
    await session.commit()
