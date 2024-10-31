from restaurant.model.models import FoodItem, NutritionFacts, db
from sqlalchemy.exc import SQLAlchemyError


class FoodDatabase:
    
    @staticmethod
    def add_food_item(food_item_data):
        try:
            db.session.add(food_item_data)
            db.session.flush()  # Flush to get the ID of the newly added food item
            return food_item_data
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error adding food item: {e}")
            raise

    @staticmethod
    def add_nutrition_facts(nutrition_facts_data):
        try:
            db.session.add(nutrition_facts_data)
            return nutrition_facts_data
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error adding nutrition facts: {e}")
            raise

    @staticmethod
    def commit_transaction():
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Transaction commit failed: {e}")
            raise
        
    @staticmethod
    def get_food_item(food_item_id, restaurant_id):
        return db.session.query(FoodItem).filter_by(id=food_item_id, restaurant_id=restaurant_id).first()

    @staticmethod
    def get_nutrition_fact(food_item_id):
        return db.session.query(NutritionFacts).filter_by(food_item_id=food_item_id).first()

