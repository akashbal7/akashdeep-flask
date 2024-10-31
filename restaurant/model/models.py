from restaurant import db, bcrypt
from flask_login import UserMixin
from datetime import datetime

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
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.id', ondelete='CASCADE'), nullable=False)
    phone_number = db.Column(db.String(15))
    website = db.Column(db.String(255))  # Website field
    sitting_capacity = db.Column(db.Integer)  # Sitting capacity field
    cuisine = db.Column(db.String(100))  # Cuisine type field
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    owner = db.relationship('User', backref=db.backref('restaurants', cascade='all, delete-orphan'))
    address = db.relationship('Address', backref=db.backref('restaurants', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<Restaurant {self.name}>'
    
class FoodItem(db.Model):
    __tablename__ = 'food_item'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=True)
    in_stock = db.Column(db.Boolean, default=True)
    nutrition_facts = db.relationship('NutritionFacts', backref='food_item', uselist=False)

class NutritionFacts(db.Model):
    __tablename__ = 'nutrition_facts'

    id = db.Column(db.Integer, primary_key=True)
    serving_size = db.Column(db.String(50), nullable=True)
    calories = db.Column(db.Integer, nullable=True)
    calories_from_fat = db.Column(db.Integer, nullable=True)
    total_fat = db.Column(db.Float, nullable=True)
    saturated_fat = db.Column(db.Float, nullable=True)
    trans_fat = db.Column(db.Float, nullable=True)
    cholesterol = db.Column(db.Integer, nullable=True)
    sodium = db.Column(db.Integer, nullable=True)
    total_carbohydrate = db.Column(db.Float, nullable=True)
    dietary_fiber = db.Column(db.Float, nullable=True)
    sugars = db.Column(db.Float, nullable=True)
    protein = db.Column(db.Float, nullable=True)
    food_item_id = db.Column(db.Integer, db.ForeignKey('food_items.id'))
