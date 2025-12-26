"""
Configuration Module

This module handles the application configuration settings.
It loads environment variables from a .env file and provides a centralized
Settings class to access them throughout the application.
It also handles database connection string adjustments for asyncpg.
"""

import os
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv()

class Settings:
    """
    Application Settings

    Attributes:
        DATABASE_URL (str): The database connection string.
        SECRET_KEY (str): The secret key used for JWT encoding/decoding.
        ALGORITHM (str): The algorithm used for JWT token generation.
        ACCESS_TOKEN_EXPIRE_MINUTES (int): The expiration time for access tokens in minutes.
    """
    DATABASE_URL = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-keep-it-secret")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def __init__(self):
        """
        Initializes the Settings class.
        
        Validates the presence of DATABASE_URL and adjusts it for asyncpg compatibility.
        """
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL is not set in .env file")

        # Ensure we are using the asyncpg driver for PostgreSQL
        # SQLAlchemy's async engine requires 'postgresql+asyncpg://' scheme
        if self.DATABASE_URL.startswith("postgresql://"):
            self.DATABASE_URL = self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

        # Fix for asyncpg: replace 'sslmode' with 'ssl' in query parameters
        # asyncpg uses 'ssl' parameter instead of 'sslmode'
        if "sslmode=" in self.DATABASE_URL:
            self.DATABASE_URL = self.DATABASE_URL.replace("sslmode=", "ssl=")

        # Fix for asyncpg: remove 'channel_binding' if present
        # asyncpg does not support 'channel_binding' parameter
        if "channel_binding=" in self.DATABASE_URL:
            self.DATABASE_URL = re.sub(r"[?&]channel_binding=[^&]+", "", self.DATABASE_URL)

# Instantiate the settings object to be used across the app
settings = Settings()
