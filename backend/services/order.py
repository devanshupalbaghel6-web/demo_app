from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from models.order import Order, OrderItem
from models.product import Product
from schemas.order import OrderCreate

async def create_order(db: AsyncSession, order: OrderCreate, user_id: int):
    db_order = Order(user_id=user_id, status="pending")
    db.add(db_order)
    await db.flush()

    for item in order.items:
        result = await db.execute(select(Product).where(Product.id == item.product_id))
        product = result.scalar_one_or_none()
        if product:
            db_item = OrderItem(
                order_id=db_order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price_at_purchase=product.price
            )
            db.add(db_item)
    
    await db.commit()
    
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.id == db_order.id)
    )
    return result.scalar_one()

async def get_orders(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items))
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def get_user_orders(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.user_id == user_id)
    )
    return result.scalars().all()
