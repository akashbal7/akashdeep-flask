from restaurant.model.models import db, Restaurant


class RestaurantDatabase:

    @staticmethod
    def get_restaurant(restaurant_id):
        try:
            restaurant = Restaurant.query.get(restaurant_id)
            if restaurant is None:
                raise ValueError(f"Restaurant with id {restaurant_id} not found.")
            return restaurant
        except Exception as e:
            print(f"Error fetching restaurant: {e}")
            raise

    @staticmethod
    def get_restaurant_by_owner_id(owner_id):
        try:
            restaurant = Restaurant.query.filter_by(owner_id=owner_id).first()
            if restaurant is None:
                raise ValueError(f"No restaurant found for owner id {owner_id}.")
            return restaurant
        except Exception as e:
            print(f"Error fetching restaurant by owner_id: {e}")
            raise

    @staticmethod
    def add_restaurant(data):
        restaurant = Restaurant(
            owner_id=data['owner_id'],
            address_id=data['address_id'],
            name=data['name'],
            phone_number=data.get('phone_number'),
            sitting_capacity=data.get('sitting_capacity'),
            cuisine=data.get('cuisine'),
            website=data.get('website')
        )
        try:
            db.session.add(restaurant)
            RestaurantDatabase.commit_transaction()
            print(f"Restaurant {restaurant.name} added successfully.")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding restaurant: {e}")
            raise

    @staticmethod
    def update_restaurant(restaurant):
        try:
            db.session.add(restaurant)
            RestaurantDatabase.commit_transaction()
            print(f"Restaurant {restaurant.name} updated successfully.")
        except Exception as e:
            db.session.rollback()
            print(f"Error updating restaurant: {e}")
            raise

    @staticmethod
    def commit_transaction():
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Transaction commit failed: {e}")
            raise
