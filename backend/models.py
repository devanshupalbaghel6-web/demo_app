from sqlalchemy import Column, Integer, String, Float, Text
from database import Base

# Define the Product model
# This class represents the 'products' table in the database
class Product(Base):
    __tablename__ = "products"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Product name
    name = Column(String, index=True)
    
    # Product description
    description = Column(Text)
    
    # Product price
    price = Column(Float)
    
    # Image URL for the product
    image_url = Column(String)
