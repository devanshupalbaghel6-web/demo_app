from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from models.base import Base

class User(Base):
    """
    User Model
    
    Represents a registered user in the system.
    Uses UUID for the primary key for better scalability and security (harder to guess IDs).
    """
    __tablename__ = "users"

    # Primary Key: UUID
    # We use uuid.uuid4 to generate a random UUID by default.
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # User's email address, must be unique.
    email = Column(String, unique=True, index=True)
    
    # Hashed password (never store plain text passwords!).
    hashed_password = Column(String)
    
    # Status flags
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    
    # Relationship to Order: One-to-Many
    # A user can have multiple orders.
    orders = relationship("Order", back_populates="user")
