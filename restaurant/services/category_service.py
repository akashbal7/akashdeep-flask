from restaurant.database.category_database import CategoryDatabase
from restaurant.database.restaurant_database import RestaurantDatabase
import logging
from restaurant.model.models import  Category

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CategoryService:
    
    @staticmethod
    def add_category(data, restaurant_id):
        try:
            restaurant = RestaurantDatabase.get_restaurant(restaurant_id)
            if not restaurant:
                print("no restaurant")
                return {
                "message": "Restaurant not found.",
                "data": None
            }, 404
                 
            category = Category(
                name=data['name'],
                description=data.get('description')
            )
            CategoryDatabase.add_category(category)
            if restaurant:
                restaurant.categories.append(category)
                CategoryDatabase.commit_transaction()
                return {
                "message": "Category added successdully",
                "category_id": category.id
            }, 200
        except Exception as e:
            print(f"Failed to add category {e}")
            raise ValueError("Failed to add category. Please check the input data and try again.")
        
    
    @staticmethod
    def get_categories_by_restaurant(restaurant_id):
        try:     
            return RestaurantDatabase.get_restaurant_categories(restaurant_id)
        except Exception as e:
            print(f"Failed to retrieve categories for restaurant {restaurant_id}: {e}")
            raise ValueError("Failed to retrieve categories.")
        
    @staticmethod
    def get_all_categories():
        try:
            return CategoryDatabase.get_all_categories()
        except Exception as e:
            print(f"Failed to retrieve all categories: {e}")
            raise ValueError("Failed to retrieve all categories.")
        
    @staticmethod
    def link_category_to_restaurant(restaurant_id, category):
        try:
            restaurant = RestaurantDatabase.get_restaurant(restaurant_id)
            if restaurant and category not in restaurant.categories:
                restaurant.categories.append(category)
                RestaurantDatabase.commit_transaction()
                return True
            return False
        except Exception as e:
            print(f"Failed to link category to restaurant: {e}")
            raise ValueError("Failed to link category to restaurant.")