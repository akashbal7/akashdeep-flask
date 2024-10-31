from flask import jsonify
from sqlalchemy.exc import IntegrityError, OperationalError
from werkzeug.security import generate_password_hash, check_password_hash
from restaurant.database.user_database import UserDatabase
from restaurant.database.restaurant_database import RestaurantDatabase
from restaurant.database.address_database import AddressDatabase
from restaurant.model.models import db
import logging

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
            return  {'message': 'Login successful', 'user_id': user.id, 'role': user.role, 'email': user.email}, 200

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
                'role': user.role,
                'phone_number': user.phone_number,
                # Add other fields as necessary
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
