import asyncio
from database import AsyncSessionLocal, engine
from models import Base, Product
from sqlalchemy import select

async def seed_data():
    # Create tables if they don't exist (just in case)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        # Check if we already have products
        result = await session.execute(select(Product))
        products = result.scalars().all()
        
        if products:
            print("Products already exist. Skipping seed.")
            return

        print("Seeding data...")
        
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
        print("Data seeded successfully!")

if __name__ == "__main__":
    asyncio.run(seed_data())
