from sqlalchemy.exc import IntegrityError, OperationalError
from werkzeug.security import generate_password_hash
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
                "country":None,
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
