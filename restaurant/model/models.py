from restaurant import db, bcrypt
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    #phone_number = db.Column(db.String(10), nullable=True, 
    #info={'check': 'LENGTH(phone_number) = 10 OR phone_number IS NULL'})
    
    __table_args__ = (
        db.CheckConstraint("role IN ('customer', 'owner')", name='check_role'),
    )

    def __repr__(self):
        return f'<User {self.email, self.first_name, self.last_name, self.role}>'
    
class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    address_line_1 = db.Column(db.String(255), nullable=False)
    address_line_2 = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

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
    created_at = Column(DateTime, default=datetime.utcnow)

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
    created_at = Column(DateTime, default=datetime.utcnow)
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
    created_at = Column(DateTime, default=datetime.utcnow)
    
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
