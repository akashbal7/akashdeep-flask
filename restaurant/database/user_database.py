from restaurant.model.models import db, User, Restaurant


class UserDatabase:
    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def get_restaurant_by_user_id(user_id):
        return Restaurant.query.filter_by(owner_id=user_id).first()

    @staticmethod
    def add_user(user_data):
        new_user = User(
            email=user_data['email'],
            password_hash=user_data['password_hash'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            role=user_data['role']
        )
        db.session.add(new_user)
        db.session.flush()
        return new_user.id  
    
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id) 
    
    @staticmethod
    def update_user(user):
        db.session.add(user)  # Commit the changes made to the user instance.

    @staticmethod
    def delete_user(user_id):
        user = UserDatabase.get_user_by_id(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def commit_transaction():
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Transaction commit failed: {e}")
            raise
