from flask import jsonify
from sqlalchemy.exc import IntegrityError, OperationalError
from werkzeug.security import generate_password_hash, check_password_hash
from restaurant.database.user_database import UserDatabase
from restaurant.database.restaurant_database import RestaurantDatabase
from restaurant.database.address_database import AddressDatabase
from restaurant.model.models import db
import logging
from restaurant.model.models import FoodItem, NutritionFacts

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserService:
    @staticmethod
    def register_user(data):
        # Validate required fields
        required_fields = ['first_name', 'last_name', 'email', 'password']
        for field in required_fields:
            if not data[field]:
                return {'error': f'{field.replace("_", " ").title()} is required'}, 400

        # Validate the role field
        role = data.get('role', 'customer')  # Default role to 'customer' if not provided
        if role not in ['customer', 'owner']:
            return {'error': 'Invalid role. Allowed values are "customer" or "owner".'}, 400
        
        if role == "owner":
            if not data["restaurant_name"]:
                return {'error': f'{"reaturant_name".replace("_", " ").title()} is required'}, 400
        

        # Check if user already exists
        if UserDatabase.get_user_by_email(data['email']):
            return {'error': 'Email already registered'}, 409

        # Hash the password
        password_hash = generate_password_hash(data['password'])

        # Create new user record
        user_data = {
            'email': data['email'],
            'password_hash': password_hash,
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'role': role
        }

        # Attempt to add the user to the database
        try:
            user_id = UserDatabase.add_user(user_data)
            if role == "owner":
                address_data = {
                "address_line_1": "demo address",
                "address_line_2":None,
                "city":None,
                "state":None,
                "postal_code":None,
                "country":None
                ,
                }

                address_id = AddressDatabase.add_address(address_data)
                logger.info(f"address id: {address_id}")

                restaurant_data = {
                'owner_id': user_id,
                "address_id":address_id,
                "name": data["restaurant_name"],
                "phone_number":None,
                "sitting_capacity":None,
                "cuisine":None,
                "website":None,
                }

                print(restaurant_data)

                restaurant_id = RestaurantDatabase.add_restaurant(restaurant_data)
                logger.info(f"restaurant id: {restaurant_id}")
            db.session.commit()
            return {'message': 'Registration successful'}, 201
        except IntegrityError as e:
            logger.error(f"Integrity error during registration: {e}")
            db.session.rollback()
            return {'error': 'Integrity error. Please check your input data.'}, 400

        except OperationalError as e:
            logger.error(f"Operational error during registration: {e}")
            db.session.rollback()
            return {'error': 'Database operation error. Please try again later.'}, 500

        except Exception as e:
            logger.error(f"Error during registration: {e}")
            db.session.rollback()
            return {'error': 'Registration failed. Please try again1.'}, 500
    
    @staticmethod
    def login_user(data):
        # Check if the user exists
        email = data.get('email')
        password = data.get('password')

        try:
            user = UserDatabase.get_user_by_email(email)

            if not user:
                return {'error': 'Invalid email or password.'}, 401

            # Verify the password
            if not check_password_hash(user.password_hash, password):
                return {'error': 'Invalid email or password.'}, 401

            # Return a success message (and possibly a token or user data)
            result = {
                'message': 'Login successful',
                'user_id': user.id, 
                'role': user.role, 
                'email': user.email,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'full_name':user.first_name + ' ' + user.last_name
            }
            return  result, 200

        except Exception as e:
            logger.error(f"Error during login: {e}")
            return {'error': 'An error occurred while trying to log in. Please try again later.'}, 500
        

    @staticmethod
    def get_user_by_id(user_id):
        try:
            user = UserDatabase.get_user_by_id(user_id)
            if user is None:
                return None, 404
            
            # Create a dictionary with user details to return
            user_data = {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role
                #'phone_number': user.phone_number,
                # Add other fields as necessary
            }

             # If the user is an owner, get their restaurant data
            if user.role == 'owner':
                restaurant = RestaurantDatabase.get_restaurant_by_owner_id(user.id)
                print("ressssssssss",restaurant.address_id)
                address = AddressDatabase.get_address_by_id(restaurant.address_id)
                if restaurant:
                    user_data['restaurant'] = {
                        'id': restaurant.id,
                        'name': restaurant.name,
                        'phone_number': restaurant.phone_number,
                        'website': restaurant.website,
                        'sitting_capacity': restaurant.sitting_capacity,
                        'cuisine': restaurant.cuisine,
                        'address': {
                            'id': address.id,
                            'address_line_1': address.address_line_1,
                            'address_line_2': address.address_line_2,
                            'city': address.city,
                            'state': address.state,
                            'postal_code': address.postal_code,
                            'country': address.country,
                        }
                    }

            return user_data, 200

        except Exception as e:
            logger.error(f"Error retrieving user: {e}")
            return {'error': 'Failed to retrieve user. Please try again later.'}, 500
        
    @staticmethod
    def edit_user(user_id, data):
        user = UserDatabase.get_user_by_id(user_id)
        if user is None:
            return None, 404

        # Update fields as necessary
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'phone_number' in data:
            user.phone_number = data['phone_number']

        # Commit the changes to the database
        print("hhhhhhhhh",user)
        try:
            UserDatabase.update_user(user)
            return {'message': 'User updated successfully.'}, 200
        except Exception as e:
            logger.error(f"Error updating user: {e}")
            db.session.rollback()
            return {'error': 'Failed to update user. Please try again later.'}, 500
        
    @staticmethod
    def update_address(address_id, data):
        # Fetch the address record by address_id    
        address = AddressDatabase.get_address_by_id(address_id)
        if address is None:
            return None, 404

        # Update address fields as necessary
        if 'address_line_1' in data:
            address.address_line_1 = data['address_line_1']
        if 'address_line_2' in data:
            address.address_line_2 = data['address_line_2']
        if 'city' in data:
            address.city = data['city']
        if 'state' in data:
            address.state = data['state']
        if 'postal_code' in data:
            address.postal_code = data['postal_code']
        if 'country' in data:
            address.country = data['country']

        # Commit the changes to the database
        try:
            AddressDatabase.update_address(address)
            return {'message': 'Address updated successfully.'}, 200
        except Exception as e:
            logger.error(f"Error updating address: {e}")
            db.session.rollback()
            return {'error': 'Failed to update address. Please try again.'}, 500

def add_food_item(data):
    food_item = FoodItem(
        name=data['name'],
        description=data.get('description'),
        price=data['price'],
        category=data.get('category'),
        in_stock=data.get('in_stock', True)
    )
    db.session.add(food_item)
    db.session.flush()

    if data.get('add_nutrition_facts'):
        nutrition_data = data.get('nutrition_facts', {})
        nutrition_facts = NutritionFacts(
            serving_size=nutrition_data.get('servingSize'),
            calories=nutrition_data.get('calories'),
            calories_from_fat=nutrition_data.get('caloriesFromFat'),
            total_fat=nutrition_data.get('totalFat'),
            saturated_fat=nutrition_data.get('saturatedFat'),
            trans_fat=nutrition_data.get('transFat'),
            cholesterol=nutrition_data.get('cholesterol'),
            sodium=nutrition_data.get('sodium'),
            total_carbohydrate=nutrition_data.get('totalCarbohydrate'),
            dietary_fiber=nutrition_data.get('dietaryFiber'),
            sugars=nutrition_data.get('sugars'),
            protein=nutrition_data.get('protein'),
            food_item_id=food_item.id
        )
        db.session.add(nutrition_facts)
    
    db.session.commit()
    return food_item