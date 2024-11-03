from restaurant.model.models import db,FoodReview,RestaurantReview
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReviewService:
    @staticmethod
    def add_review(restaurant_id, rating,  review_text):
        review = RestaurantReview(
            restaurant_id=restaurant_id,
            rating=rating,
            review_text=review_text
        )
        db.session.add(review)
        db.session.commit()
        return review

    @staticmethod
    def get_reviews(restaurant_id):
        return RestaurantReview.query.filter_by(restaurant_id=restaurant_id).all()
    
    @staticmethod
    def add_food_reviews(food_item_id,rating,taste_rating,texture_rating,quality_rating,presentation_rating,review_text):
        food_reviews = FoodReview(
            food_item_id = food_item_id,
            rating = rating,
            taste_rating = taste_rating,
            texture_rating = texture_rating,
            quality_rating = quality_rating,
            presentation_rating = presentation_rating,
            review_text = review_text
        )
        db.session.add(food_reviews)
        db.session.commit()
        return food_reviews
    
    @staticmethod
    def get_food_reviews(food_item_id):
        return FoodReview.query.filter_by(food_item_id=food_item_id).all()
    