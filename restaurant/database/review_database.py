from restaurant.model.models import FoodItem, db, RestaurantReview, FoodReview


class ReviewDatabase:
    
    @staticmethod
    def create_review(customer_id, restaurant_id, rating,experience_rating=0,value_rating=0,service_rating=0,food_rating=0, review_text=None):
        # Create and return a new RestaurantReview object
        review = RestaurantReview(
            customer_id=customer_id,
            restaurant_id=restaurant_id,
            rating=rating,
            experience_rating=experience_rating,
            value_rating=value_rating,
            service_rating=service_rating,
            food_rating=food_rating,
            review_text=review_text
        )
        db.session.add(review)
        return review
    
    @staticmethod
    def get_reviews_by_restaurant(restaurant_id):
        # Query to get all reviews for the specified restaurant
        return RestaurantReview.query.filter_by(restaurant_id=restaurant_id).all()
    
    @staticmethod
    def create_food_review(customer_id, food_item_id, rating, taste_rating=None, texture_rating=None, 
                           quality_rating=None, presentation_rating=None, review_text=None):
        
        food_review = FoodReview(
            customer_id=customer_id,
            food_item_id=food_item_id,
            rating=rating,
            taste_rating=taste_rating,
            texture_rating=texture_rating,
            quality_rating=quality_rating,
            presentation_rating=presentation_rating,
            review_text=review_text
        )
        
        db.session.add(food_review)
        return food_review
    
    @staticmethod
    def get_reviews_by_food(food_item_id):
        return FoodReview.query.filter_by(food_item_id=food_item_id).all()
    
    @staticmethod
    def get_food_reviews_by_restaurant(restaurant_id):
        # Query to get all reviews for the specified restaurant
        reviews = db.session.query(FoodReview, FoodItem).join(FoodItem).filter(FoodItem.restaurant_id == restaurant_id).all()
        return reviews

    @staticmethod
    def commit_transaction():
        db.session.commit()
    
    @staticmethod
    def rollback_transaction():
        db.session.rollback()