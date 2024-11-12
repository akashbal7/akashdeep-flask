from sqlalchemy import func
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
    def get_food_item(food_item_id):
        try:
            return FoodItem.query.get(food_item_id)
        except Exception as e:
            print(f"Error retrieving food item with ID {food_item_id}: {e}")
            raise ValueError("Failed to retrieve food item.")

    @staticmethod
    def get_nutrition_fact(food_item_id):
        try:
            return db.session.query(NutritionFacts).filter_by(food_item_id=food_item_id).first()
        except Exception as e:
            print(f"Error retrieving nutrition facts for food item ID {food_item_id}: {e}")
            raise ValueError("Failed to retrieve nutrition facts.")

    @staticmethod
    def delete_food_item(food_item):
        try:
            db.session.delete(food_item)
        except Exception as e:
            print(f"Error deleting food item with ID {food_item.id}: {e}")
            raise ValueError("Failed to delete food item.")

    @staticmethod
    def delete_nutrition_fact(nutrition_fact):
        try:
            db.session.delete(nutrition_fact)
        except Exception as e:
            print(f"Error deleting nutrition facts for food item ID {nutrition_fact.food_item_id}: {e}")
            raise ValueError("Failed to delete nutrition facts.")

    @staticmethod
    def rollback_transaction():
        try:
            db.session.rollback()
        except Exception as e:
            print(f"Error rolling back transaction: {e}")
            raise ValueError("Failed to rollback transaction.")
        
    @staticmethod
    def get_restaurant_food_list(restaurant_id):
        try:
            return FoodItem.query.filter_by(restaurant_id=restaurant_id).all()
        except Exception as e:
            print(f"Error fetching food list: {e}")
            raise ValueError("Database error when retrieving food list.")
        
    @staticmethod
    def get_all_foods(category=None):
        try:
            query = FoodItem.query
            if category:
              query = query.filter(func.lower(FoodItem.category) == func.lower(category))
            items = query.all()
            return items
        except Exception as e:
            print(f"Error fetching all food items: {e}")
            raise ValueError("Database error when retrieving all food items.")
        
    @staticmethod
    def get_nutrition_fact(food_item_id):
        try:
            return db.session.query(NutritionFacts).filter_by(food_item_id=food_item_id).first()
        except Exception as e:
            print(f"Database error when retrieving food Nutrition Fact.: {e}")
            raise ValueError("Unable to getch Nutrition Fact.")

