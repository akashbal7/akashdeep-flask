from restaurant.database.food_database import FoodDatabase
import logging, os, base64
from werkzeug.utils import secure_filename
from restaurant.model.models import FoodItem, NutritionFacts, Category
from flask import json, request, jsonify, current_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}



class FoodService:
    
    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    @staticmethod
    def add_food_item(data, restaurant_id, image_file):
        print("data", data)
        try:
            has_nutrition_fact = data.get('has_nutrition_fact', 'false').lower() == 'true'
            availability = data.get('in_stock', 'false').lower() == 'true'
            upload_folder = current_app.config['UPLOAD_FOLDER']
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            image_filename = ""
            
            if image_file and FoodService.allowed_file(image_file.filename):
                image_filename = secure_filename(image_file.filename)
                # Use current_app to get the UPLOAD_FOLDER configuration
                image_path = os.path.join(upload_folder, image_filename)
                image_file.save(image_path)  # Save the image file
                print("image_path", image_path)
            
            # Create FoodItem object
            food_item = FoodItem(
                restaurant_id=restaurant_id,
                name=data['name'],
                description=data.get('description'),
                price=float(data['price']),
                availability=availability,
                has_nutrition_fact=has_nutrition_fact,
                image_filename=image_filename
            )

            # Add food item to the database and flush to get the ID
            FoodDatabase.add_food_item(food_item)
            print(data['nutrition_fact'])
            # # Optionally add nutrition facts
            if has_nutrition_fact:
                nutrition_data = json.loads(data.get('nutrition_fact', '{}'))
                nutrition_facts = NutritionFacts(
                    food_item_id=food_item.id,
                    serving_size=nutrition_data.get('serving_size'),
                    calories=nutrition_data.get('calories'),
                    calories_from_fat=nutrition_data.get('calories_from_fat'),
                    total_fat_g=nutrition_data.get('total_fat'),
                    saturated_fat_g=nutrition_data.get('saturated_fat'),
                    trans_fat_g=nutrition_data.get('trans_fat'),
                    cholesterol_mg=nutrition_data.get('cholesterol'),
                    sodium_mg=nutrition_data.get('sodium'),
                    total_carbohydrate_g=nutrition_data.get('total_carbohydrate'),
                    dietary_fiber_g=nutrition_data.get('dietary_fiber'),
                    sugars_g=nutrition_data.get('sugars'),
                    protein_g=nutrition_data.get('protein')
                )
                for attr, value in nutrition_facts.__dict__.items():
                    if value == '':
                        setattr(nutrition_facts, attr, None)

            


                # Add nutrition facts to the database
                FoodDatabase.add_nutrition_facts(nutrition_facts)
                
            category_ids = json.loads(data.get('categories', '[]'))
            if category_ids:
                categories = Category.query.filter(Category.id.in_(category_ids)).all()
                food_item.categories.extend(categories)

            # Commit the transaction
            FoodDatabase.commit_transaction()
            
            return food_item

        except Exception as e:
            print(f"Failed to add food item and nutrition facts: {e}")
            raise ValueError("Failed to add food item. Please check the input data and try again.")
        
    @staticmethod
    def get_food_item(restaurant_id, food_item_id):
        try:
            reviews=[]
            total_reviews = None
            average_rating = None
            texture_rating = None
            quality_rating = None
            presentation_rating = None
            taste_rating = None
            upload_folder = current_app.config['UPLOAD_FOLDER']
            food_item = FoodDatabase.get_food_item(food_item_id)
            reviews = [review.to_dict() for review in food_item.reviews]
            if reviews:
                total_reviews = len(reviews)
                if total_reviews > 0:
                    average_rating = sum(review['rating'] for review in reviews) / total_reviews
                    texture_rating = sum(review['texture_rating'] for review in reviews) / total_reviews
                    quality_rating = sum(review['quality_rating'] for review in reviews) / total_reviews
                    presentation_rating = sum(review['presentation_rating'] for review in reviews) / total_reviews
                    taste_rating = sum(review['taste_rating'] for review in reviews) / total_reviews
                
            if not food_item:
                raise ValueError("Food item not found.")
            if food_item.image_filename:
                with open(f"{upload_folder}/{food_item.image_filename}", "rb") as img_file:
                        encoded_image = base64.b64encode(img_file.read()).decode('utf-8')
            else:
                encoded_image = None
                
            if food_item:
                food_item_data = {
                    "id": food_item.id,
                    "restaurant_id": food_item.restaurant_id,
                    "name": food_item.name,
                    "description": food_item.description,
                    "price": food_item.price,
                    "in_stock": food_item.availability,
                    "has_nutrition_fact": food_item.has_nutrition_fact,
                    "total_reviews": total_reviews,
                    "average_rating": average_rating,
                    "presentation_rating": presentation_rating,
                    "quality_rating": quality_rating,
                    "texture_rating": texture_rating,
                    "taste_rating": taste_rating,
                    "image_data": encoded_image,  
                    "categories":[category.to_dict() for category in food_item.categories]
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
            food_item = FoodDatabase.get_food_item(food_item_id)
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
            food_item = FoodDatabase.get_food_item(food_item_id)
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
        
    @staticmethod
    def get_restaurant_food_list(restaurant_id):
        try:
            food_items = FoodDatabase.get_restaurant_food_list(restaurant_id)
            food_list = []
            
            for food_item in food_items:
                item_data = {
                    "id": food_item.id,
                    "name": food_item.name,
                    "description": food_item.description,
                    "price": food_item.price,
                    "in_stock": food_item.availability,
                    "categories":[category.to_dict() for category in food_item.categories] 
                }
                
                # Optionally add nutrition facts
                nutrition_fact = FoodDatabase.get_nutrition_fact(food_item.id)
                if nutrition_fact:
                    item_data["nutrition_facts"] = nutrition_fact.to_dict()
                
                food_list.append(item_data)
                
            return food_list
        except Exception as e:
            print(f"Error retrieving food list: {e}")
            raise ValueError("Failed to retrieve food list.")
        
    @staticmethod
    def get_all_foods(category):
        try:
            upload_folder = current_app.config['UPLOAD_FOLDER']
            food_items = FoodDatabase.get_all_foods(category)
            all_foods = []
            for food_item in food_items:
                if food_item.image_filename:
                    with open(f"{upload_folder}/{food_item.image_filename}", "rb") as img_file:
                        encoded_image = base64.b64encode(img_file.read()).decode('utf-8')
                else:
                    encoded_image = None

                all_foods.append({
                    "id": food_item.id,
                    "restaurant_id": food_item.restaurant_id,
                    "name": food_item.name,
                    "description": food_item.description,
                    "price": food_item.price,
                    "in_stock": food_item.availability,
                    "has_nutrition_fact": food_item.has_nutrition_fact,
                    "categories":[category.to_dict() for category in food_item.categories],
                    "image_data": encoded_image  # Send Base64 data
                })

            # Return all food items with the total count
            return {"foods": all_foods, "total_count": len(all_foods)}
        except Exception as e:
            print(f"Error retrieving all foods: {e}")
            raise ValueError("Failed to retrieve food items.")
        
    @staticmethod
    def get_food_nutrition_fact(food_item_id):
        try:
            # Fetch the nutrition fact for the given food item
            nutrition_fact = FoodDatabase.get_nutrition_fact(food_item_id)
            
            # If the nutrition fact exists, return it as a dictionary
            if not nutrition_fact:
                raise ValueError("Nutrition facts Unavailable.")
                
            return nutrition_fact.to_dict()
                
        except Exception as e:
            print(f"Error retrieving nutrition facts: {e}")
            raise ValueError(str(e))



