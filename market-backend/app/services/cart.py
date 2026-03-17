from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.exceptions import ConflictException, NotFoundException
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.product import Product
from app.models.user import User
from app.schemas.cart import CartItemCreate, CartItemUpdate


async def get_my_cart(session: AsyncSession, current_user: User):
    result = await session.exec(select(Cart).where(Cart.user_id == current_user.id))
    cart = result.first()
    if not cart:
        raise NotFoundException("Cart not found")
    return cart


async def add_to_cart(session: AsyncSession, current_user: User, data: CartItemCreate):
    cart = await get_my_cart(session, current_user)
    product = await session.get(Product, data.product_id)
    if not product or not product.is_active:
        raise NotFoundException("Product not found")
    if product.stock < data.quantity:
        raise ConflictException("Requested quantity exceeds stock")

    existing = await session.exec(
        select(CartItem).where(CartItem.cart_id == cart.id, CartItem.product_id == data.product_id)
    )
    item = existing.first()

    if item:
        new_qty = item.quantity + data.quantity
        if new_qty > product.stock:
            raise ConflictException("Total quantity in cart exceeds stock")
        item.quantity = new_qty
        session.add(item)
    else:
        item = CartItem(cart_id=cart.id, product_id=data.product_id, quantity=data.quantity)
        session.add(item)

    await session.commit()
    await session.refresh(item)
    return item


async def update_cart_item(session: AsyncSession, current_user: User, item_id, data: CartItemUpdate):
    item = await session.get(CartItem, item_id)
    if not item:
        raise NotFoundException("Cart item not found")

    cart = await get_my_cart(session, current_user)
    if item.cart_id != cart.id:
        raise NotFoundException("Cart item not found in your cart")

    product = await session.get(Product, item.product_id)
    if data.quantity > product.stock:
        raise ConflictException("Requested quantity exceeds stock")

    item.quantity = data.quantity
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


async def remove_cart_item(session: AsyncSession, current_user: User, item_id):
    item = await session.get(CartItem, item_id)
    if not item:
        raise NotFoundException("Cart item not found")

    cart = await get_my_cart(session, current_user)
    if item.cart_id != cart.id:
        raise NotFoundException("Cart item not found in your cart")

    await session.delete(item)
    await session.commit()
