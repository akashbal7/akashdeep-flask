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
    
    __table_args__ = (
        db.CheckConstraint("role IN ('customer', 'owner')", name='check_role'),
    )

    def __repr__(self):
        return f'<User {self.email}>'
    
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
