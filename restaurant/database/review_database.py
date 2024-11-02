from sqlalchemy import Column, Integer, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from restaurant.model.models import db

class ReviewDatabase(db.Model):
    __tablename__ = 'reviews'

    id = Column(db.Integer, primary_key=True)
    restaurant_id = Column(db.Integer, ForeignKey('restaurants.id'), nullable=False)  # Match 'restaurants' table name
    food_rating = db.Column(db.Float, nullable=False)
    service_rating = db.Column(db.Float, nullable=False)
    value_rating = db.Column(db.Float, nullable=False)
    atmosphere_rating = db.Column(db.Float, nullable=False)
    review_text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())

    # Define the relationship to Restaurant
    restaurant = db.relationship("Restaurant", back_populates="reviews")  # Use 'restaurant' here
