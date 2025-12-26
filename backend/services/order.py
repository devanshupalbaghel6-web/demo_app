"""
Order Service Module

This module contains the business logic for managing orders in the application.
It handles the creation, retrieval, and processing of orders and their associated items.
It interacts directly with the database using SQLAlchemy's async session.
"""

# Import AsyncSession for type hinting the database session
from sqlalchemy.ext.asyncio import AsyncSession
# Import select for constructing SQL queries
from sqlalchemy.future import select
# Import selectinload for eager loading of related data (relationships)
from sqlalchemy.orm import selectinload
# Import the SQLAlchemy models for Order and OrderItem
from models.order import Order, OrderItem
# Import the Product model to fetch price information
from models.product import Product
# Import the Pydantic schema for order creation validation
from schemas.order import OrderCreate
# Import UUID for handling unique identifiers
from uuid import UUID

async def create_order(db: AsyncSession, order: OrderCreate, user_id: UUID):
    """
    Creates a new order in the database.

    This function performs the following steps:
    1. Creates a new Order record associated with the user.
    2. Sets the initial status of the order to 'completed' (assuming immediate payment/fulfillment for this demo).
    3. Iterates through the items provided in the order payload.
    4. Fetches the current price of each product from the database to ensure data integrity (snapshotting the price).
    5. Creates OrderItem records linking the order to the products.
    6. Commits the transaction to save changes.
    7. Refreshes and returns the created order with its items loaded.

    Args:
        db (AsyncSession): The database session for executing queries.
        order (OrderCreate): The Pydantic model containing order details (list of items).
        user_id (UUID): The unique identifier of the user placing the order.

    Returns:
        Order: The newly created order object, including its items.
    """
    # Create a new Order instance. 
    # We set status to "completed" immediately as per requirements to avoid "pending" state in this demo.
    db_order = Order(user_id=user_id, status="completed")
    
    # Add the new order to the session. 
    # This does not yet commit it to the database, but prepares it for insertion.
    db.add(db_order)
    
    # Flush the session to generate the ID for db_order without committing the transaction.
    # This allows us to use db_order.id when creating OrderItems.
    await db.flush()

    # Iterate over each item in the order request
    for item in order.items:
        # Query the database to find the product by its ID
        result = await db.execute(select(Product).where(Product.id == item.product_id))
        product = result.scalar_one_or_none()
        
        # If the product exists, create an OrderItem
        if product:
            db_item = OrderItem(
                order_id=db_order.id,       # Link to the newly created order
                product_id=item.product_id, # Link to the product
                quantity=item.quantity,     # Set the quantity ordered
                price_at_purchase=product.price # Snapshot the price at the time of purchase
            )
            # Add the order item to the session
            db.add(db_item)
    
    # Commit the transaction to save the Order and all OrderItems to the database permanently.
    await db.commit()
    
    # Retrieve the newly created order from the database.
    # We use selectinload(Order.items) to eagerly load the related items, 
    # ensuring they are available in the response.
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.id == db_order.id)
    )
    
    # Return the single scalar result (the Order object)
    return result.scalar_one()

async def get_orders(db: AsyncSession, skip: int = 0, limit: int = 100):
    """
    Retrieves a list of orders from the database with pagination.

    Args:
        db (AsyncSession): The database session.
        skip (int): The number of records to skip (for pagination). Default is 0.
        limit (int): The maximum number of records to return. Default is 100.

    Returns:
        List[Order]: A list of Order objects, with their items eagerly loaded.
    """
    # Execute a select query on the Order table
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items)) # Eagerly load the 'items' relationship
        .offset(skip)   # Apply offset for pagination
        .limit(limit)   # Apply limit for pagination
    )
    # Return all scalar results as a list
    return result.scalars().all()

async def get_user_orders(db: AsyncSession, user_id: UUID):
    """
    Retrieves all orders belonging to a specific user.

    Args:
        db (AsyncSession): The database session.
        user_id (UUID): The unique identifier of the user.

    Returns:
        List[Order]: A list of Order objects for the specified user.
    """
    # Execute a select query filtering by user_id
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items)) # Eagerly load items
        .where(Order.user_id == user_id)    # Filter by the user's ID
    )
    # Return all matching orders
    return result.scalars().all()
