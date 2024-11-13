from sqlalchemy import func
from restaurant.model.models import Category, db
from sqlalchemy.exc import SQLAlchemyError


class CategoryDatabase:
    
    @staticmethod
    def add_category(category):
        try:
            db.session.add(category)
            db.session.flush()
            return category
        except Exception as e:
            db.session.rollback()
            print(f"Error adding food item: {e}")
            raise
        
    @staticmethod
    def get_all_categories():
        try:
            return Category.query.all()
        except SQLAlchemyError as e:
            print(f"Error retrieving all categories: {e}")
            raise
        
    @staticmethod
    def get_category_by_name(name):
        return Category.query.filter(func.lower(Category.name) == name.lower()).first()

    @staticmethod
    def commit_transaction():
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Transaction commit failed: {e}")
            raise
        
    @staticmethod
    def rollback_transaction():
        try:
            db.session.rollback()
        except Exception as e:
            print(f"Error rolling back transaction: {e}")
            raise ValueError("Failed to rollback transaction.")