from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.exceptions import ConflictException, NotFoundException
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


async def create_category(session: AsyncSession, data: CategoryCreate):
    existing = await session.exec(select(Category).where(Category.name == data.name))
    if existing.first():
        raise ConflictException("Category already exists")

    category = Category(**data.model_dump())
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category


async def list_categories(session: AsyncSession):
    result = await session.exec(select(Category).order_by(Category.name))
    return result.all()


async def update_category(session: AsyncSession, category_id, data: CategoryUpdate):
    category = await session.get(Category, category_id)
    if not category:
        raise NotFoundException("Category not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(category, key, value)

    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category


async def delete_category(session: AsyncSession, category_id):
    category = await session.get(Category, category_id)
    if not category:
        raise NotFoundException("Category not found")
    await session.delete(category)
    await session.commit()
