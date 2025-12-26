from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import engine
from models import base
from routes import product, user, order, auth

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(base.Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "Welcome to the E-commerce API"}

# Include routers
app.include_router(auth.router)
app.include_router(product.router)
app.include_router(user.router)
app.include_router(order.router)

