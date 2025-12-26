from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.orm import relationship
from models.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    price = Column(Float)
    image_url = Column(String)

    # Relationship to OrderItem
    order_items = relationship("OrderItem", back_populates="product")
