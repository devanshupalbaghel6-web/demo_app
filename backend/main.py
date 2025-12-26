"""
Main Application Entry Point

This module initializes the FastAPI application, configures middleware (CORS),
sets up database tables on startup, and includes the various API routers.
"""

# Import FastAPI framework
from fastapi import FastAPI
# Import CORSMiddleware to handle Cross-Origin Resource Sharing
from fastapi.middleware.cors import CORSMiddleware
# Import the database engine from the core configuration
from core.database import engine
# Import the base model to access metadata for table creation
from models import base
# Import the API route modules
from routes import product, user, order, auth

# Initialize the FastAPI application instance
app = FastAPI(
    title="E-Commerce API",
    description="A comprehensive API for an e-commerce platform handling users, products, and orders.",
    version="1.0.0"
)

# Configure CORS (Cross-Origin Resource Sharing)
# This is essential for allowing the frontend (running on a different port) to communicate with this backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. In production, replace with specific frontend URL (e.g., ["http://localhost:5173"])
    allow_credentials=True, # Allows cookies and authentication headers
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Event handler for application startup
@app.on_event("startup")
async def startup():
    """
    Startup event handler.
    
    This function runs when the application starts.
    It connects to the database and creates all tables defined in the SQLAlchemy models
    if they do not already exist.
    """
    # Begin a connection to the database
    async with engine.begin() as conn:
        # Run the synchronous create_all method in an async context
        # This inspects the metadata of all imported models and generates CREATE TABLE statements
        await conn.run_sync(base.Base.metadata.create_all)

# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint to verify the API is running.
    
    Returns:
        dict: A welcome message.
    """
    return {"message": "Welcome to the E-commerce API"}

# Include the routers for different functional areas
# This organizes the API endpoints into logical groups
app.include_router(auth.router)    # Authentication endpoints (login, token)
app.include_router(product.router) # Product management endpoints
app.include_router(user.router)    # User management endpoints
app.include_router(order.router)   # Order processing endpoints

