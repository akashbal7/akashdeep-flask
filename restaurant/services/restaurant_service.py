from restaurant.database.restaurant_database import RestaurantDatabase
from restaurant.database.user_database import UserDatabase
import logging

logger = logging.getLogger(__name__)

class RestaurantService:
    @staticmethod
    def update_restaurant(data, restaurant_id):
        try:
            # Fetch the restaurant by ID
            restaurant = RestaurantDatabase.get_restaurant(restaurant_id)
            if not restaurant:
                raise ValueError("Restaurant not found.")

            # Update restaurant fields
            restaurant.name = data.get('restaurant_name', restaurant.name)
            restaurant.phone_number = data.get('phone_number', restaurant.phone_number)
            restaurant.website = data.get('website', restaurant.website)
            restaurant.about = data.get('about', restaurant.about)
            restaurant.sitting_capacity = data.get('sitting_capacity', restaurant.sitting_capacity)

            # Update user details (owner)
            user = UserDatabase.get_user_by_id(restaurant.owner_id)
            if not user:
                raise ValueError("User not found.")
            if user:
                user.first_name = data.get('first_name', user.first_name)
                user.last_name = data.get('last_name', user.last_name)
                UserDatabase.update_user(user)

            # Commit the changes
            RestaurantDatabase.update_restaurant(restaurant)
            RestaurantDatabase.commit_transaction()
            
            return restaurant
        except ValueError as e:
            raise ValueError(str(e))
        
        except Exception as e:
            print(f"Failed to update restaurant: {e}")
            raise ValueError("Failed to update restaurant details.")
        