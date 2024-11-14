from restaurant.database.restaurant_database import RestaurantDatabase
from restaurant.database.user_database import UserDatabase
from restaurant.database.address_database import AddressDatabase
import logging, os, base64
from werkzeug.utils import secure_filename
from flask import json, request, jsonify, current_app

logger = logging.getLogger(__name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

class RestaurantService:
    
    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    @staticmethod
    def update_restaurant(data, restaurant_id, image_file):
        try:
            upload_folder = current_app.config['UPLOAD_FOLDER']
            print("folderrrrrrr", upload_folder)
            if not os.path.isdir(upload_folder):
                logger.info(f"Creating folder: {upload_folder}")
                # os.makedirs(upload_folder)
            image_filename = ""
            
            if image_file and RestaurantService.allowed_file(image_file.filename):
                image_filename = secure_filename(image_file.filename)
                # Use current_app to get the UPLOAD_FOLDER configuration
                image_path = os.path.join(upload_folder, image_filename)
                image_file.save(image_path)  # Save the image file
                print("image_path", image_path)
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
            restaurant.image_filename = data.get('image_filename',image_filename )

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
        
    @staticmethod
    def get_restaurants():
        try:
            upload_folder = current_app.config['UPLOAD_FOLDER']
            restaurants = RestaurantDatabase.get_all_restaurants()
            all_restaurants = []
            reviews = []
            total_reviews = None
            average_rating = None
            
            for restaurant in restaurants:
                if restaurant.image_filename:
                    with open(f"{upload_folder}/{restaurant.image_filename}", "rb") as img_file:
                        encoded_image = base64.b64encode(img_file.read()).decode('utf-8')
                else:
                    encoded_image = None
                
                reviews = [review.to_dict() for review in restaurant.reviews]
                if reviews:
                    total_reviews = len(reviews)
                    if total_reviews > 0:
                        average_rating = sum(review['rating'] for review in reviews) / total_reviews

                all_restaurants.append({
                    "id": restaurant.id,
                    "name": restaurant.name,
                    "about": restaurant.about,
                    "phone_number": restaurant.phone_number,
                    "website": restaurant.website,
                    "sitting_capacity": restaurant.sitting_capacity,
                    "average_rating": average_rating,
                    "total_reviews": total_reviews,
                    "categories":[category.to_dict() for category in restaurant.categories],
                    "image_data": encoded_image  # Send Base64 data
                })

            # Return all food items with the total count
            return {"data": all_restaurants, "total_count": len(all_restaurants)}, 200
        except Exception as e:
            print(f"Error retrieving all restaurants: {e}")
            raise ValueError("Failed to retrieve all restaurants.")
        
    @staticmethod
    def get_restaurant(restaurant_id):
        try:
            upload_folder = current_app.config['UPLOAD_FOLDER']
            service_rating = None
            value_rating = None
            food_rating = None
            total_reviews = None
            experience_rating = None
            average_rating = None
            # Fetch the restaurant instance
            restaurant = RestaurantDatabase.get_restaurant(restaurant_id)
            if not restaurant:
                return {
                    "message": "Restaurant not found.",
                    "data": {}
                }, 404
            
            # Convert restaurant instance to dictionary if to_dict() exists
            restaurant_data = restaurant.to_dict()

            # Encode the image if it exists
            if restaurant.image_filename:
                with open(f"{upload_folder}/{restaurant.image_filename}", "rb") as img_file:
                    restaurant_data['image_data'] = base64.b64encode(img_file.read()).decode('utf-8')
            else:
                restaurant_data['image_data'] = None

            # Add reviews and categories to the dictionary
            reviews = [review.to_dict() for review in restaurant.reviews]
            categories = [category.to_dict() for category in restaurant.categories]
            
            # Calculate total reviews and average rating
            if reviews:
                total_reviews = len(reviews)
                if total_reviews > 0:
                    average_rating = sum(review['rating'] for review in reviews) / total_reviews
                    food_rating = sum(review['food_rating'] for review in reviews) / total_reviews
                    service_rating = sum(review['service_rating'] for review in reviews) / total_reviews
                    value_rating = sum(review['value_rating'] for review in reviews) / total_reviews
                    experience_rating = sum(review['experience_rating'] for review in reviews) / total_reviews

            # Update restaurant_data with additional fields
            restaurant_data.update({
                "reviews": reviews,
                "categories": categories,
                "experience_rating": experience_rating,
                "value_rating": value_rating,
                "service_rating": service_rating,
                "food_rating": food_rating,
                "average_rating": average_rating,
                "total_reviews": total_reviews
            })

            # Add address to the dictionary
            address = AddressDatabase.get_address_by_id(restaurant.address_id)
            if address:
                restaurant_data["address"] = address.to_dict()

            return {
                "message": "Restaurant fetched successfully.",
                "data": restaurant_data
            }, 200

        except Exception as e:
            logger.error(f"Error retrieving restaurant: {e}")
            return {'error': 'Failed to retrieve restaurant. Please try again later.'}, 500