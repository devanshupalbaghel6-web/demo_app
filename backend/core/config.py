import os
from dotenv import load_dotenv
import re

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")

    def __init__(self):
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL is not set in .env file")

        # Ensure we are using the asyncpg driver
        if self.DATABASE_URL.startswith("postgresql://"):
            self.DATABASE_URL = self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

        # Fix for asyncpg: replace 'sslmode' with 'ssl' in query parameters
        if "sslmode=" in self.DATABASE_URL:
            self.DATABASE_URL = self.DATABASE_URL.replace("sslmode=", "ssl=")

        # Fix for asyncpg: remove 'channel_binding' if present
        if "channel_binding=" in self.DATABASE_URL:
            self.DATABASE_URL = re.sub(r"[?&]channel_binding=[^&]+", "", self.DATABASE_URL)

settings = Settings()
