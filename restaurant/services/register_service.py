from sqlalchemy.exc import IntegrityError, OperationalError
from werkzeug.security import generate_password_hash, check_password_hash
from restaurant.database.user_database import UserDatabase
from restaurant.database.restaurant_database import RestaurantDatabase
from restaurant.database.address_database import AddressDatabase
from restaurant.database.food_database import FoodDatabase
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
            return {"user_id" : user_id,'message': 'Registration successful'}, 201
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
                return None

            # Verify the password
            if not check_password_hash(user.password_hash, password):
                return {'error': 'Invalid email or password.'}, 401
            user_dict = user.to_dict()
            if user_dict['role'] == "owner":
                restaurant = UserDatabase.get_restaurant_by_user_id(user.id)
                user_dict['restaurant_id'] = restaurant.id if restaurant else None
            return user_dict

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
            user_data = user.to_dict()

             # If the user is an owner, get their restaurant data
            if user_data['role'] == 'owner':
                restaurant = RestaurantDatabase.get_restaurant_by_owner_id(user.id)
                address = AddressDatabase.get_address_by_id(restaurant.address_id)
                if restaurant:
                    user_data['restaurant'] = {
                        'id': restaurant.id,
                        'name': restaurant.name,
                        'phone_number': restaurant.phone_number,
                        'website': restaurant.website,
                        'sitting_capacity': restaurant.sitting_capacity,
                        'about': restaurant.about,
                        'cuisine': restaurant.cuisine,
                        'address': address.to_dict()
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

        try:
            UserDatabase.update_user(user)
            UserDatabase.commit_transaction()
            
            return {
                    "message": "User updated successfully.",
                    "data": user.to_dict()
                }, 200
        
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
            food_item = FoodDatabase.get_food_item(food_item_id)
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
            raise ValueError("Failed to delete food item.")


