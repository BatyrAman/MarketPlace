from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.exceptions import ForbiddenException, NotFoundException
from app.models.category import Category
from app.models.product import Product
from app.models.user import User, UserRole
from app.schemas.product import ProductCreate, ProductUpdate


async def create_product(session: AsyncSession, seller: User, data: ProductCreate):
    if seller.role not in [UserRole.seller, UserRole.admin]:
        raise ForbiddenException("Only seller or admin can create products")

    category = await session.get(Category, data.category_id)
    if not category:
        raise NotFoundException("Category not found")

    product = Product(**data.model_dump(), seller_id=seller.id)
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


async def list_products(
    session: AsyncSession,
    search: str | None = None,
    category_id=None,
    sort_by: str = "created_at",
    order: str = "desc",
):
    stmt = select(Product).where(Product.is_active == True)

    if search:
        stmt = stmt.where(Product.name.ilike(f"%{search}%"))
    if category_id:
        stmt = stmt.where(Product.category_id == category_id)

    sort_column = getattr(Product, sort_by, Product.created_at)
    stmt = stmt.order_by(sort_column.desc() if order == "desc" else sort_column.asc())

    result = await session.exec(stmt)
    return result.all()


async def get_product(session: AsyncSession, product_id):
    product = await session.get(Product, product_id)
    if not product or not product.is_active:
        raise NotFoundException("Product not found")
    return product


async def update_product(session: AsyncSession, current_user: User, product_id, data: ProductUpdate):
    product = await session.get(Product, product_id)
    if not product:
        raise NotFoundException("Product not found")

    if current_user.role != UserRole.admin and product.seller_id != current_user.id:
        raise ForbiddenException("You can update only your own products")

    updates = data.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(product, key, value)

    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


async def delete_product(session: AsyncSession, current_user: User, product_id):
    product = await session.get(Product, product_id)
    if not product:
        raise NotFoundException("Product not found")

    if current_user.role != UserRole.admin and product.seller_id != current_user.id:
        raise ForbiddenException("You can delete only your own products")

    product.is_active = False
    session.add(product)
    await session.commit()
