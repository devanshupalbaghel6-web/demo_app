from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.product import Product
from schemas.product import ProductCreate
from uuid import UUID

async def get_products(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Product).offset(skip).limit(limit))
    return result.scalars().all()

async def get_product(db: AsyncSession, product_id: UUID):
    result = await db.execute(select(Product).where(Product.id == product_id))
    return result.scalar_one_or_none()

async def create_product(db: AsyncSession, product: ProductCreate):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

async def update_product(db: AsyncSession, product_id: UUID, product: ProductCreate):
    db_product = await get_product(db, product_id)
    if db_product:
        for key, value in product.model_dump().items():
            setattr(db_product, key, value)
        await db.commit()
        await db.refresh(db_product)
    return db_product

async def delete_product(db: AsyncSession, product_id: UUID):
    db_product = await get_product(db, product_id)
    if db_product:
        await db.delete(db_product)
        await db.commit()
    return db_product
