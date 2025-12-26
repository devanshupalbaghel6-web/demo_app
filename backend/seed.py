import asyncio
from core.database import AsyncSessionLocal, engine
from models.base import Base
from models.product import Product
from models.user import User
from models.order import Order, OrderItem
from sqlalchemy import select
from utils.security import get_password_hash

async def seed_data():
    # Drop all tables to ensure a clean slate for UUID changes
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        # Check if we already have products
        result = await session.execute(select(Product))
        products = result.scalars().all()
        
        if not products:
            print("Seeding products...")
            
            # Create some dummy products
            product_list = [
                Product(
                    name="Minimalist Watch",
                    description="A simple, elegant watch for everyday wear.",
                    price=120.00,
                    image_url="https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=500&q=60"
                ),
                Product(
                    name="Leather Backpack",
                    description="Durable leather backpack with plenty of storage.",
                    price=85.50,
                    image_url="https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=500&q=60"
                ),
                Product(
                    name="Wireless Headphones",
                    description="High-quality sound with noise cancellation.",
                    price=199.99,
                    image_url="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=500&q=60"
                ),
                Product(
                    name="Ceramic Coffee Mug",
                    description="Handcrafted ceramic mug for your morning brew.",
                    price=25.00,
                    image_url="https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?auto=format&fit=crop&w=500&q=60"
                ),
                 Product(
                    name="Running Shoes",
                    description="Lightweight and comfortable shoes for running.",
                    price=110.00,
                    image_url="https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=500&q=60"
                ),
            ]

            session.add_all(product_list)
            await session.commit()
            print("Products seeded successfully!")
            
            # Refresh products to get IDs
            result = await session.execute(select(Product))
            products = result.scalars().all()
        else:
            print("Products already exist. Skipping product seed.")

        # Check if we have users
        result = await session.execute(select(User))
        users = result.scalars().all()
        
        if not users:
            print("Seeding users...")
            
            admin_user = User(
                email="admin@example.com",
                hashed_password=get_password_hash("admin123"),
                is_admin=True
            )
            
            regular_user = User(
                email="user@example.com",
                hashed_password=get_password_hash("user123"),
                is_admin=False
            )
            
            session.add(admin_user)
            session.add(regular_user)
            await session.commit()
            print("Users seeded successfully!")
            
            # Create a sample order for the regular user
            print("Seeding orders...")
            order = Order(
                user_id=regular_user.id,
                status="completed"
            )
            session.add(order)
            await session.flush() # Get order ID

            # Add items to order
            if products:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=products[0].id,
                    quantity=1,
                    price_at_purchase=products[0].price
                )
                session.add(order_item)
                await session.commit()
                print("Orders seeded successfully!")

            await session.flush()
            
            # Add items to the order
            if products:
                item1 = OrderItem(
                    order_id=order.id,
                    product_id=products[0].id,
                    quantity=1,
                    price_at_purchase=products[0].price
                )
                item2 = OrderItem(
                    order_id=order.id,
                    product_id=products[1].id,
                    quantity=2,
                    price_at_purchase=products[1].price
                )
                session.add(item1)
                session.add(item2)
                await session.commit()
                print("Orders seeded successfully!")
        else:
            print("Users already exist. Skipping user seed.")

if __name__ == "__main__":
    asyncio.run(seed_data())
