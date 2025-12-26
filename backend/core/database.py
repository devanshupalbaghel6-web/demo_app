"""
Database Configuration

This module sets up the database connection using SQLAlchemy's async engine.
It provides the session factory and the base class for ORM models.
"""

# Import SQLAlchemy's async engine and session components
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# Import sessionmaker to create a session factory
from sqlalchemy.orm import sessionmaker, declarative_base
# Import application settings (including database URL)
from core.config import settings

# Create the async database engine
# echo=True enables logging of all generated SQL statements (useful for debugging)
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Create a configured "Session" class
# This factory will generate new AsyncSession instances for each request
AsyncSessionLocal = sessionmaker(
    bind=engine,            # Bind the session to our engine
    class_=AsyncSession,    # Use the async session class
    expire_on_commit=False  # Prevent attributes from expiring after commit (needed for async)
)

# Create a Base class for our models to inherit from
# All model classes (User, Product, Order) will inherit from this Base
Base = declarative_base()

# Dependency to get the database session
async def get_db():
    """
    Dependency generator that yields a database session.
    
    This function is used by FastAPI dependencies to provide a database session
    to route handlers. It ensures the session is properly closed after the request is processed.
    
    Yields:
        AsyncSession: An active database session.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            # Ensure the session is closed even if an error occurs
            await session.close()
