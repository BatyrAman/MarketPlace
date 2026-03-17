from decimal import Decimal
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.exceptions import ConflictException, NotFoundException, ForbiddenException
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.user import User, UserRole


async def create_order_from_cart(session: AsyncSession, current_user: User):
    cart_result = await session.exec(select(Cart).where(Cart.user_id == current_user.id))
    cart = cart_result.first()
    if not cart:
        raise NotFoundException("Cart not found")

    items_result = await session.exec(select(CartItem).where(CartItem.cart_id == cart.id))
    cart_items = items_result.all()
    if not cart_items:
        raise ConflictException("Cart is empty")

    total = Decimal("0.00")
    order = Order(user_id=current_user.id, total_amount=Decimal("0.00"))
    session.add(order)
    await session.flush()

    for cart_item in cart_items:
        product = await session.get(Product, cart_item.product_id)
        if not product or not product.is_active:
            raise ConflictException(f"Product {cart_item.product_id} is unavailable")
        if product.stock < cart_item.quantity:
            raise ConflictException(f"Insufficient stock for product {product.name}")

        product.stock -= cart_item.quantity
        session.add(product)

        item_total = product.price * cart_item.quantity
        total += item_total

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=cart_item.quantity,
            price_at_purchase=product.price,
        )
        session.add(order_item)

    order.total_amount = total
    session.add(order)

    for cart_item in cart_items:
        await session.delete(cart_item)

    await session.commit()
    await session.refresh(order)
    return order


async def list_my_orders(session: AsyncSession, current_user: User):
    result = await session.exec(select(Order).where(Order.user_id == current_user.id).order_by(Order.created_at.desc()))
    return result.all()


async def get_order(session: AsyncSession, current_user: User, order_id):
    order = await session.get(Order, order_id)
    if not order:
        raise NotFoundException("Order not found")

    if current_user.role != UserRole.admin and order.user_id != current_user.id:
        raise ForbiddenException("You can only access your own orders")

    return order


async def update_order_status(session: AsyncSession, current_user: User, order_id, status: OrderStatus):
    order = await session.get(Order, order_id)
    if not order:
        raise NotFoundException("Order not found")

    if current_user.role != UserRole.admin:
        raise ForbiddenException("Only admin can update order status")

    order.status = status
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order
