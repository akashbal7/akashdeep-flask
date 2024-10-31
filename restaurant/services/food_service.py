from restaurant.database.food_database import FoodDatabase
import logging
from restaurant.model.models import FoodItem, NutritionFacts

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FoodService:
    
    @staticmethod
    def add_food_item(data, restaurant_id):
        try:
            # Create FoodItem object
            food_item = FoodItem(
                restaurant_id=restaurant_id,
                name=data['name'],
                description=data.get('description'),
                price=data['price'],
                category=data.get('category'),
                availability=data.get('in_stock', True)
            )

            # Add food item to the database and flush to get the ID
            FoodDatabase.add_food_item(food_item)

            # Optionally add nutrition facts
            if data.get('nutrition_fact'):
                nutrition_data = data.get('nutrition_fact', {})
                nutrition_facts = NutritionFacts(
                    food_item_id=food_item.id,
                    serving_size=nutrition_data.get('serving_size'),
                    calories=nutrition_data.get('calories'),
                    calories_from_fat=nutrition_data.get('calories_from_fat'),
                    total_fat_g=nutrition_data.get('total_fat'),
                    total_fat_percent=nutrition_data.get('total_fat_percent'),
                    saturated_fat_g=nutrition_data.get('saturated_fat'),
                    saturated_fat_percent=nutrition_data.get('saturated_fat_percent'),
                    trans_fat_g=nutrition_data.get('trans_fat'),
                    cholesterol_mg=nutrition_data.get('cholesterol'),
                    cholesterol_percent=nutrition_data.get('cholesterol_percent'),
                    sodium_mg=nutrition_data.get('sodium'),
                    sodium_percent=nutrition_data.get('sodium_percent'),
                    total_carbohydrate_g=nutrition_data.get('total_carbohydrate'),
                    carbohydrate_percent=nutrition_data.get('carbohydrate_percent'),
                    dietary_fiber_g=nutrition_data.get('dietary_fiber'),
                    fiber_percent=nutrition_data.get('fiber_percent'),
                    sugars_g=nutrition_data.get('sugars'),
                    protein_g=nutrition_data.get('protein')
                )

               


                # Add nutrition facts to the database
                FoodDatabase.add_nutrition_facts(nutrition_facts)

            # Commit the transaction
            FoodDatabase.commit_transaction()
            
            return food_item

        except Exception as e:
            print(f"Failed to add food item and nutrition facts: {e}")
            raise ValueError("Failed to add food item. Please check the input data and try again.")
        
    @staticmethod
    def get_food_item(restaurant_id, food_item_id):
        try:
            food_item = FoodDatabase.get_food_item(food_item_id, restaurant_id)
            if not food_item:
                raise ValueError("Food item not found.")
            if food_item:
                food_item_data = {
                    "id": food_item.id,
                    "restaurant_id": food_item.restaurant_id,
                    "name": food_item.name,
                    "description": food_item.description,
                    "price": food_item.price,
                    "category": food_item.category,
                    "in_stock": food_item.availability,
                }
                nutrition_fact = FoodDatabase.get_nutrition_fact(food_item_id)
                if nutrition_fact:  # Changed from plural to singular
                    food_item_data["nutrition_facts"] = nutrition_fact.to_dict()  # Directly use the nutrition fact object
                else:
                    food_item_data["nutrition_facts"] = {}  # Handle case where no nutrition fact exists
                return food_item_data
            else:
                raise ValueError("Food item not found.")

        except Exception as e:
            print(f"Error retrieving food item: {e}")
            raise
    
    @staticmethod
    def update_food_item(data, restaurant_id, food_item_id):
        try:
            food_item = FoodDatabase.get_food_item(food_item_id, restaurant_id)
            if not food_item:
                raise ValueError("Food item not found.")

            # Update food item fields
            food_item.name = data.get('name', food_item.name)
            food_item.description = data.get('description', food_item.description)
            food_item.price = data.get('price', food_item.price)
            food_item.category = data.get('category', food_item.category)
            food_item.availability = data.get('in_stock', food_item.availability)

            # Update nutrition facts if provided
            if data.get('nutrition_fact'):
                nutrition_data = data.get('nutrition_fact', {})
                nutrition_fact = FoodDatabase.get_nutrition_fact(food_item_id)

                if nutrition_fact:
                    # Update existing nutrition facts
                    nutrition_fact.serving_size = nutrition_data.get('serving_size', nutrition_fact.serving_size)
                    nutrition_fact.calories = nutrition_data.get('calories', nutrition_fact.calories)
                    nutrition_fact.calories_from_fat = nutrition_data.get('calories_from_fat', nutrition_fact.calories_from_fat)
                    nutrition_fact.total_fat_g = nutrition_data.get('total_fat_g', nutrition_fact.total_fat_g)
                    nutrition_fact.total_fat_percent = nutrition_data.get('total_fat_percent', nutrition_fact.total_fat_percent)
                    nutrition_fact.saturated_fat_g = nutrition_data.get('saturated_fat_g', nutrition_fact.saturated_fat_g)
                    nutrition_fact.saturated_fat_percent = nutrition_data.get('saturated_fat_percent', nutrition_fact.saturated_fat_percent)
                    nutrition_fact.trans_fat_g = nutrition_data.get('trans_fat_g', nutrition_fact.trans_fat_g)
                    nutrition_fact.cholesterol_mg = nutrition_data.get('cholesterol_mg', nutrition_fact.cholesterol_mg)
                    nutrition_fact.cholesterol_percent = nutrition_data.get('cholesterol_percent', nutrition_fact.cholesterol_percent)
                    nutrition_fact.sodium_mg = nutrition_data.get('sodium_mg', nutrition_fact.sodium_mg)
                    nutrition_fact.sodium_percent = nutrition_data.get('sodium_percent', nutrition_fact.sodium_percent)
                    nutrition_fact.total_carbohydrate_g = nutrition_data.get('total_carbohydrate_g', nutrition_fact.total_carbohydrate_g)
                    nutrition_fact.carbohydrate_percent = nutrition_data.get('carbohydrate_percent', nutrition_fact.carbohydrate_percent)
                    nutrition_fact.dietary_fiber_g = nutrition_data.get('dietary_fiber_g', nutrition_fact.dietary_fiber_g)
                    nutrition_fact.fiber_percent = nutrition_data.get('fiber_percent', nutrition_fact.fiber_percent)
                    nutrition_fact.sugars_g = nutrition_data.get('sugars_g', nutrition_fact.sugars_g)
                    nutrition_fact.protein_g = nutrition_data.get('protein_g', nutrition_fact.protein_g)
                else:
                    # If no nutrition fact exists, create a new one
                    nutrition_fact = NutritionFacts(
                        food_item_id=food_item.id,
                        serving_size=nutrition_data.get('serving_size'),
                        calories=nutrition_data.get('calories'),
                        calories_from_fat=nutrition_data.get('calories_from_fat'),
                        total_fat_g=nutrition_data.get('total_fat_g'),
                        total_fat_percent=nutrition_data.get('total_fat_percent'),
                        saturated_fat_g=nutrition_data.get('saturated_fat_g'),
                        saturated_fat_percent=nutrition_data.get('saturated_fat_percent'),
                        trans_fat_g=nutrition_data.get('trans_fat_g'),
                        cholesterol_mg=nutrition_data.get('cholesterol_mg'),
                        cholesterol_percent=nutrition_data.get('cholesterol_percent'),
                        sodium_mg=nutrition_data.get('sodium_mg'),
                        sodium_percent=nutrition_data.get('sodium_percent'),
                        total_carbohydrate_g=nutrition_data.get('total_carbohydrate_g'),
                        carbohydrate_percent=nutrition_data.get('carbohydrate_percent'),
                        dietary_fiber_g=nutrition_data.get('dietary_fiber_g'),
                        fiber_percent=nutrition_data.get('fiber_percent'),
                        sugars_g=nutrition_data.get('sugars_g'),
                        protein_g=nutrition_data.get('protein_g')
                    )
                    FoodDatabase.add_nutrition_facts(nutrition_fact)

            # Commit the changes
            FoodDatabase.commit_transaction()
            return food_item.to_dict()

        except Exception as e:
            print(f"Failed to update food item and nutrition facts: {e}")
            raise ValueError("Failed to update food item. Please check the input data and try again.")
        

    @staticmethod
    def delete_food_item(restaurant_id, food_item_id):
        try:
            food_item = FoodDatabase.get_food_item(food_item_id, restaurant_id)
            if not food_item:
                print("innnnnnn")
                raise ValueError("Food item not found.")

            # Delete associated nutrition facts
            nutrition_fact = FoodDatabase.get_nutrition_fact(food_item_id)
            if nutrition_fact:
                FoodDatabase.delete_nutrition_fact(nutrition_fact)

            # Delete the food item
            FoodDatabase.delete_food_item(food_item)
            
            # Commit the changes
            FoodDatabase.commit_transaction()

        except Exception as e:
            FoodDatabase.rollback_transaction
            print(f"Failed to delete food item: {e}")
            raise ValueError(str(e))


