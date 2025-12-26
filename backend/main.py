from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from fastapi.middleware.cors import CORSMiddleware

import models
import schemas
from database import get_db, engine

app = FastAPI()

# Configure CORS to allow requests from our React frontend
# In a real app, you might want to restrict this to specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Create tables on startup (for simplicity, usually done via Alembic)
# We will still set up Alembic, but this is a quick way to get started
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "Welcome to the E-commerce API"}

# Get all products
@app.get("/products", response_model=List[schemas.Product])
async def get_products(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    # Use SQLAlchemy select statement
    result = await db.execute(select(models.Product).offset(skip).limit(limit))
    products = result.scalars().all()
    return products

# Create a product
@app.post("/products", response_model=schemas.Product)
async def create_product(product: schemas.ProductCreate, db: AsyncSession = Depends(get_db)):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

# Get a single product
@app.get("/products/{product_id}", response_model=schemas.Product)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Product).where(models.Product.id == product_id))
    product = result.scalar_one_or_none()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
