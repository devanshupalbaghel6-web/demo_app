from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the database URL from environment variables
# We use 'postgresql+asyncpg' scheme for async support
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env file")

# Ensure we are using the asyncpg driver
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# Fix for asyncpg: replace 'sslmode' with 'ssl' in query parameters
if "sslmode=" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("sslmode=", "ssl=")

# Fix for asyncpg: remove 'channel_binding' if present (not supported by asyncpg directly via SQLAlchemy)
if "channel_binding=" in DATABASE_URL:
    # Remove channel_binding parameter. It might be at the end or in the middle.
    # Simple replace might leave a trailing & or ? if not careful, but let's try simple first.
    # Regex would be better but let's stick to string manipulation for simplicity if possible.
    import re
    DATABASE_URL = re.sub(r"[?&]channel_binding=[^&]+", "", DATABASE_URL)

# Create the async engine
# echo=True will log all SQL queries to the console (good for debugging)
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a configured "Session" class
# expire_on_commit=False is important for async sessions
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Create a Base class for our models to inherit from
Base = declarative_base()

# Dependency to get the database session
# This will be used in our FastAPI path operations
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
