"""
User Database Model

This module defines the SQLAlchemy model for the 'users' table.
It represents the structure of user data stored in the PostgreSQL database.
"""

# Import SQLAlchemy Column types for defining table schema
from sqlalchemy import Column, String, Boolean
# Import PostgreSQL specific UUID type for efficient UUID storage
from sqlalchemy.dialects.postgresql import UUID
# Import relationship to define associations between tables
from sqlalchemy.orm import relationship
# Import python's built-in uuid module for generating default UUIDs
import uuid
# Import the shared Base class for declarative models
from models.base import Base

class User(Base):
    """
    User Model
    
    Represents a registered user in the system.
    Inherits from the declarative Base class.
    
    Attributes:
        id (UUID): The primary key, a unique identifier for the user. Generated automatically.
        email (str): The user's email address. Must be unique across the system. Indexed for fast lookups.
        hashed_password (str): The securely hashed password. Plain text passwords are never stored.
        is_active (bool): Flag to indicate if the user account is active. Defaults to True.
        is_admin (bool): Flag to indicate if the user has administrative privileges. Defaults to False.
        orders (list[Order]): A relationship to the Order model, representing the list of orders placed by this user.
    """
    # The name of the table in the database
    __tablename__ = "users"

    # Primary Key: UUID
    # as_uuid=True ensures that SQLAlchemy converts the database value to a Python UUID object.
    # default=uuid.uuid4 sets the default value to a new random UUID if not provided.
    # index=True creates an index on this column for faster query performance.
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # User's email address
    # unique=True enforces a database-level constraint that no two users can have the same email.
    email = Column(String, unique=True, index=True)
    
    # Hashed password
    # We store the hash (e.g., bcrypt) rather than the actual password for security.
    hashed_password = Column(String)
    
    # Status flags
    # is_active can be used to soft-delete or ban users without removing the record.
    is_active = Column(Boolean, default=True)
    # is_admin determines access to protected administrative endpoints.
    is_admin = Column(Boolean, default=False)
    
    # Relationship to Order: One-to-Many
    # This allows accessing user.orders to get a list of Order objects.
    # "User" is the name of this class (implicit backref context).
    orders = relationship("Order", back_populates="user")
    # A user can have multiple orders.
    orders = relationship("Order", back_populates="user")
