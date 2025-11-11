"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Pizza app schemas

class Pizza(BaseModel):
    """
    Pizza menu items
    Collection name: "pizza"
    """
    name: str = Field(..., description="Pizza name")
    description: Optional[str] = Field(None, description="Short description")
    price_small: float = Field(..., ge=0, description="Small size price")
    price_medium: float = Field(..., ge=0, description="Medium size price")
    price_large: float = Field(..., ge=0, description="Large size price")
    vegetarian: bool = Field(False, description="Is vegetarian")
    image: Optional[str] = Field(None, description="Image URL")

class OrderItem(BaseModel):
    pizza_id: str = Field(..., description="ID of the pizza")
    size: str = Field(..., description="Size selected: small|medium|large")
    quantity: int = Field(1, ge=1, description="Quantity of this pizza")
    unit_price: float = Field(..., ge=0, description="Unit price at time of order")
    name: str = Field(..., description="Pizza name snapshot")

class Order(BaseModel):
    """
    Orders placed by customers
    Collection name: "order"
    """
    customer_name: str = Field(..., description="Customer full name")
    customer_phone: str = Field(..., description="Contact phone number")
    customer_address: str = Field(..., description="Delivery address")
    items: List[OrderItem] = Field(..., description="List of items in the order")
    subtotal: float = Field(..., ge=0, description="Subtotal of items")
    delivery_fee: float = Field(0, ge=0, description="Delivery fee")
    total: float = Field(..., ge=0, description="Total amount paid")
    status: str = Field("pending", description="Order status: pending|preparing|delivering|completed|cancelled")

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
