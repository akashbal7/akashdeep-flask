from restaurant.model.models import db, Restaurant


class RestaurantDatabase:

    @staticmethod
    def get_restaurant(restaurant_id):
        try:
            return Restaurant.query.get(restaurant_id)
        except Exception as e:
            print(f"Error fetching restaurant: {e}")
            raise
    
    @staticmethod
    def get_restaurant_by_owner_id(owner_id):
        return Restaurant.query.filter_by(owner_id=owner_id).first()
    
    @staticmethod
    def update_restaurant(restaurant):
        db.session.add(restaurant) 
        
    @staticmethod
    def commit_transaction():
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Transaction commit failed: {e}")
            raise
