from restaurant.model.models import db, User


class UserDatabase:
    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

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
