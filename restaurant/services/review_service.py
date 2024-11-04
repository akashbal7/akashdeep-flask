from restaurant.database.review_database import ReviewDatabase
from restaurant.database.restaurant_database import RestaurantDatabase
from restaurant.database.food_database import FoodDatabase
import logging

logger = logging.getLogger(__name__)

class ReviewService:
    @staticmethod
    def add_review(data, customer_id, restaurant_id):
        try:
            # Validate rating
            if data['rating'] < 1 or data['rating'] > 5:
                return {
                    "message": "Rating must be between 1 and 5.",
                    "data": {}
                }, 400
            
            # Use database layer to create the review object
            review = ReviewDatabase.create_review(
                customer_id=customer_id,
                restaurant_id=restaurant_id,
                rating=data['rating'],
                review_text=data.get('review_text')
            )
            
            # Commit the transaction to save the review
            ReviewDatabase.commit_transaction()

            return {
                "message": "Review added successfully.",
                "data": {
                    "id": review.id,
                    "customer_id": review.customer_id,
                    "restaurant_id": review.restaurant_id,
                    "rating": review.rating,
                    "review_text": review.review_text,
                    "created_at": review.created_at
                }
            }, 201

        except Exception as e:
            ReviewDatabase.rollback_transaction()
            print(f"Failed to add review: {e}")
            return {
                "message": "Failed to add review. Please try again.",
                "data": {}
            }, 500
            
    @staticmethod
    def get_restaurant_reviews(restaurant_id):
        try:
            # Fetch reviews from the database layer
            if not RestaurantDatabase.get_restaurant(restaurant_id):
                 return {
                "message": "Restaurant not found.",
                "data": []
            }, 404
            
            reviews = ReviewDatabase.get_reviews_by_restaurant(restaurant_id)

            # Prepare the response data
            reviews_data = [
                {
                    "id": review.id,
                    "customer_id": review.customer_id,
                    "restaurant_id": review.restaurant_id,
                    "rating": review.rating,
                    "review_text": review.review_text,
                    "created_at": review.created_at
                }
                for review in reviews
            ]

            return {
                "message": "Restaurant reviews retrieved successfully.",
                "data": reviews_data
            }, 200

        except Exception as e:
            print(f"Failed to retrieve restaurant reviews: {e}")
            return {
                "message": str(e),
                "data": {}
            }, 500
            
    @staticmethod
    def add_food_review(data, customer_id, food_item_id):
        try:
            # Validate main rating
            if data['rating'] < 1 or data['rating'] > 5:
                return {
                    "message": "Rating must be between 1 and 5.",
                    "data": {}
                }, 400

            # Create and add the review object via database layer
            food_review = ReviewDatabase.create_food_review(
                customer_id=customer_id,
                food_item_id=food_item_id,
                rating=data['rating'],
                taste_rating=data.get('taste_rating'),
                texture_rating=data.get('texture_rating'),
                quality_rating=data.get('quality_rating'),
                presentation_rating=data.get('presentation_rating'),
                review_text=data.get('review_text')
            )

            # Commit the transaction
            ReviewDatabase.commit_transaction()

            return {
                "message": "Food review added successfully.",
                "data": {
                    "id": food_review.id,
                    "customer_id": food_review.customer_id,
                    "food_item_id": food_review.food_item_id
                }
            }, 201

        except Exception as e:
            ReviewDatabase.rollback_transaction()
            print(f"Failed to add food review: {e}")
            return {
                "message": "Failed to add food review. Please try again.",
                "data": {}
            }, 500
            
    @staticmethod
    def get_food_reviews(food_item_id):
        try:
            # Retrieve reviews from the database
            food_item = FoodDatabase.get_food_item(food_item_id)
            if not food_item:
                return {
                "message": "Food item not found.",
                "data": []
            }, 404
                
            reviews = ReviewDatabase.get_reviews_by_food(food_item_id)

            # Format response data
            reviews_data = [
                {
                    "id": review.id,
                    "customer_id": review.customer_id,
                    "food_item_id": review.food_item_id,
                    "rating": review.rating,
                    "taste_rating": review.taste_rating,
                    "texture_rating": review.texture_rating,
                    "quality_rating": review.quality_rating,
                    "presentation_rating": review.presentation_rating,
                    "review_text": review.review_text,
                    "created_at": review.created_at
                }
                for review in reviews
            ]

            return {
                "message": "Food reviews retrieved successfully.",
                "data": reviews_data
            }, 200

        except Exception as e:
            print(f"Failed to retrieve food reviews: {e}")
            return {
                "message": "Failed to retrieve food reviews. Please try again.",
                "data": {}
            }, 500