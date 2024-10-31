from restaurant.model.models import db, Restaurant


class RestaurantDatabase:

    @staticmethod
    def add_restaurant(restaurant_data):
        new_restaurant = Restaurant(
        owner_id=restaurant_data['owner_id'],
        name=restaurant_data['name'],
        address_id=restaurant_data['address_id'],
        phone_number=restaurant_data['phone_number'],
        website=restaurant_data['website'],
        sitting_capacity=restaurant_data['sitting_capacity'],
        cuisine=restaurant_data['cuisine']
    )
        db.session.add(new_restaurant)
        db.session.flush()
        return new_restaurant.id
    
    @staticmethod
    def get_restaurant_by_owner_id(owner_id):
        return Restaurant.query.filter_by(owner_id=owner_id).first()
