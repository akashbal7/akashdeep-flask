from restaurant.database.restaurant_database import RestaurantDatabase
import logging

logger = logging.getLogger(__name__)

class RestaurantService:
    @staticmethod
    def edit_restaurant_profile(data):
        # Validate required fields for the restaurant
        required_fields = ['owner_id', 'name', 'address_id']
        for field in required_fields:
            if not data.get(field):
                return {'error': f'{field.replace("_", " ").title()} is required'}, 400

        # Additional validation for optional fields can be added here if needed

        # Prepare the restaurant data for insertion
        restaurant_data = {
            'owner_id': data['owner_id'],  # Direct access using square brackets
            'name': data['name'],
            'address_id': data['address_id'],
            'phone_number': data['phone_number'],  # Optional, can be None if not provided
            'website': data['website'],            # Optional
            'sitting_capacity': data['sitting_capacity'],  # Optional
            'cuisine': data['cuisine']             # Optional
        }


        # Attempt to add the restaurant to the database
        try:
            restaurant = RestaurantDatabase.add_restaurant(restaurant_data)
            return {'message': 'Restaurant added successfully', 'restaurant_id': restaurant.id}, 201
        except Exception as e:
            logger.error(f"Error adding restaurant: {e}")
            return {'error': 'Failed to add restaurant. Please try again.'}, 500
    