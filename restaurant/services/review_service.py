from restaurant.database.review_database import ReviewDatabase, db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReviewService:
    @staticmethod
    def add_review(restaurant_id, food, service, value, atmosphere, review_text):
        review = ReviewDatabase(
            restaurant_id=restaurant_id,
            food_rating=food,
            service_rating=service,
            value_rating=value,
            atmosphere_rating=atmosphere,
            review_text=review_text
        )
        db.session.add(review)
        db.session.commit()
        return review

    @staticmethod
    def get_reviews(restaurant_id):
        return ReviewDatabase.query.filter_by(restaurant_id=restaurant_id).all()
