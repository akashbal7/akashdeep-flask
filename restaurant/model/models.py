from restaurant import db
from flask_login import UserMixin
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, DECIMAL, Text, CheckConstraint
from sqlalchemy.orm import relationship, backref
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    role = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False, default='active')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    def to_dict(self):
        """Convert the User object to a dictionary."""
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "role": self.role,
            "full_name": self.first_name + " " + self.last_name,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    #phone_number = db.Column(db.String(10), nullable=True, 
    #info={'check': 'LENGTH(phone_number) = 10 OR phone_number IS NULL'})
    
    __table_args__ = (
        CheckConstraint("role IN ('customer', 'owner')", name='check_role'),
        CheckConstraint("status IN ('active', 'inactive', 'suspended')", name='check_status')
    )
    
    def get_by_email(self, email):
        """Get a user by email"""
        user = db.users.find_one({"email": email, "active": True})
        if not user:
            return
        user["_id"] = str(user["id"])
        return user
    
    def login(self, email, password):
        """Login a user"""
        user = self.get_by_email(email)
        if not user or not check_password_hash(user["password"], password):
            return
        user.pop("password")
        return user
    
    def get_by_id(self, user_id):
        """Get a user by id"""
        user = db.users.find_one({"id": user_id, "active": True})
        if not user:
            return
        user["id"] = str(user["id"])
        user.pop("password")
        return user

    def __repr__(self):
        return f'<User {self.email}, {self.first_name}, {self.last_name}, {self.role}, {self.status}>'
    
class Address(db.Model):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    address_line_1 = Column(String(255), nullable=False)
    address_line_2 = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    postal_code = Column(String(20))
    country = Column(String(100))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Address {self.address_line_1}, {self.city}>'
    
    


class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(100), nullable=False)
    address_id = Column(Integer, ForeignKey('addresses.id', ondelete='CASCADE'), nullable=False)
    phone_number = Column(String(15))
    website = Column(String(255))  # Website field
    sitting_capacity = Column(Integer)  # Sitting capacity field
    cuisine = Column(String(100))  # Cuisine type field
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    owner = relationship('User', backref=backref('restaurants', cascade='all, delete-orphan'))
    address = relationship('Address', backref=backref('restaurants', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<Restaurant {self.name}>'
    
class FoodItem(db.Model):
    __tablename__ = 'food_items'  # Corrected table name
    
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id', ondelete='CASCADE'))
    name = Column(String(100), nullable=False)
    description = Column(String(200), nullable=True)
    price = Column(Float, nullable=False)
    availability = Column(Boolean, default=True)
    category = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    nutrition_facts = relationship('NutritionFacts', backref='food_item', uselist=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "restaurant_id": self.restaurant_id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "category": self.category,
            "availability": self.availability,
        }

class NutritionFacts(db.Model):
    __tablename__ = 'nutrition_facts'

    id = Column(Integer, primary_key=True)
    food_item_id = Column(Integer, ForeignKey('food_items.id', ondelete='CASCADE'))
    serving_size = Column(String(50), nullable=True)
    calories = Column(Integer, nullable=True)
    calories_from_fat = Column(Integer, nullable=True)
    total_fat_g = Column(Float, nullable=True)
    total_fat_percent = Column(Integer, nullable=True)
    saturated_fat_g = Column(Float, nullable=True)
    saturated_fat_percent = Column(Integer, nullable=True)
    trans_fat_g = Column(Float, nullable=True)
    cholesterol_mg = Column(Integer, nullable=True)
    cholesterol_percent = Column(Integer, nullable=True)
    sodium_mg = Column(Integer, nullable=True)
    sodium_percent = Column(Integer, nullable=True)
    total_carbohydrate_g = Column(Float, nullable=True)
    carbohydrate_percent = Column(Integer, nullable=True)
    dietary_fiber_g = Column(Float, nullable=True)
    fiber_percent = Column(Integer, nullable=True)
    sugars_g = Column(Float, nullable=True)
    protein_g = Column(Float, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    def to_dict(self):
        return {
            "food_item_id": self.food_item_id,
            "serving_size": self.serving_size,
            "calories": self.calories,
            "calories_from_fat": self.calories_from_fat,
            "total_fat_g": self.total_fat_g,
            "total_fat_percent": self.total_fat_percent,
            "saturated_fat_g": self.saturated_fat_g,
            "saturated_fat_percent": self.saturated_fat_percent,
            "trans_fat_g": self.trans_fat_g,
            "cholesterol_mg": self.cholesterol_mg,
            "cholesterol_percent": self.cholesterol_percent,
            "sodium_mg": self.sodium_mg,
            "sodium_percent": self.sodium_percent,
            "total_carbohydrate_g": self.total_carbohydrate_g,
            "carbohydrate_percent": self.carbohydrate_percent,
            "dietary_fiber_g": self.dietary_fiber_g,
            "fiber_percent": self.fiber_percent,
            "sugars_g": self.sugars_g,
            "protein_g": self.protein_g,
            "created_at": self.created_at.isoformat()  # Convert datetime to string
        }

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id', ondelete='CASCADE'), nullable=False)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    status = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    payment_status = Column(Boolean, default=False)

    # Relationships
    customer = relationship('User', backref=backref('orders', cascade='all, delete-orphan'))
    restaurant = relationship('Restaurant', backref=backref('orders', cascade='all, delete-orphan'))
    order_items = relationship('OrderItem', backref='order', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Order {self.id}, Customer {self.customer_id}, Status {self.status}>'

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    food_item_id = Column(Integer, ForeignKey('food_items.id', ondelete='CASCADE'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_at_order = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    food_item = relationship('FoodItem', backref=backref('order_items', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<OrderItem {self.id}, Order {self.order_id}, Quantity {self.quantity}>'

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    food_item_id = Column(Integer, ForeignKey('food_items.id', ondelete='CASCADE'), nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete='CASCADE'), nullable=True)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    customer = relationship('User', backref=backref('cart_items', cascade='all, delete-orphan'))
    food_item = relationship('FoodItem', backref=backref('cart_items', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<CartItem {self.id}, Customer {self.customer_id}, Quantity {self.quantity}>'

class FoodReview(db.Model):
    __tablename__ = 'food_reviews'
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    food_item_id = Column(Integer, ForeignKey('food_items.id', ondelete='CASCADE'), nullable=False)
    rating = Column(Integer, nullable=False)
    taste_rating = Column(Integer, nullable=True)
    texture_rating = Column(Integer, nullable=True)
    quality_rating = Column(Integer, nullable=True)
    presentation_rating = Column(Integer, nullable=True)
    review_text = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    customer = relationship('User', backref=backref('food_reviews', cascade='all, delete-orphan'))
    food_item = relationship('FoodItem', backref=backref('food_reviews', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<FoodReview {self.id}, Customer {self.customer_id}, Rating {self.rating}>'

class RestaurantReview(db.Model):
    __tablename__ = 'restaurant_reviews'
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id', ondelete='CASCADE'), nullable=False)
    rating = Column(Integer, nullable=False)
    review_text = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    customer = relationship('User', backref=backref('restaurant_reviews', cascade='all, delete-orphan'))
    restaurant = relationship('Restaurant', backref=backref('restaurant_reviews', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<RestaurantReview {self.id}, Customer {self.customer_id}, Rating {self.rating}>'

class JWTToken(db.Model):
    __tablename__ = 'jwt_tokens'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    token = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)

    # Relationships
    user = relationship('User', backref=backref('jwt_tokens', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<JWTToken {self.id}, User {self.user_id}>'

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete='CASCADE'), nullable=False)
    payment_method = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    amount = Column(DECIMAL(10, 2), nullable=False)
    transaction_id = Column(String(100), unique=True, nullable=False)
    status = Column(String(20), nullable=False, default='pending')
    
    __table_args__ = (
        CheckConstraint("payment_method IN ('credit_card', 'debit_card', 'stripe', 'paypal')", name='check_payment_method'),
        CheckConstraint("status IN ('pending', 'completed', 'failed')", name='check_payment_status')
    )

    # Relationships
    order = relationship('Order', backref=backref('payments', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<Payment {self.id}, Order {self.order_id}, Amount {self.amount}>'