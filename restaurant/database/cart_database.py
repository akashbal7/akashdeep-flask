from sqlalchemy import func
from restaurant.model.models import CartItem, db
from sqlalchemy.exc import SQLAlchemyError


class CartDatabase:
    
    @staticmethod
    def get_cart_by_id(user_id):
        return CartItem.query.get(user_id)
    
    @staticmethod
    def get_cart_item(customer_id, food_item_id):
        try:
            return CartItem.query.filter_by(customer_id=customer_id, food_item_id=food_item_id).filter(CartItem.order_id.is_(None)).first()
        except SQLAlchemyError as e:
            print(f"Database query error: {e}")
            raise ValueError("Error occurred while retrieving cart item.")

    @staticmethod
    def add_cart_item(customer_id, food_item_id, quantity):
        try:
            # Create CartItem object
            cart_item = CartItem(
                customer_id=customer_id,
                food_item_id=food_item_id,
                quantity=quantity
            )
            db.session.add(cart_item)
            db.session.flush()  # Ensures cart_item ID is available if needed
            return cart_item
        except SQLAlchemyError as e:
            CartDatabase.rollback_transaction()
            print(f"Error adding cart item: {e}")
            raise ValueError("Error occurred while adding item to cart.")

    @staticmethod
    def update_cart_item(cart_item):
        try:
            db.session.add(cart_item)  # Update without adding a new object
            return cart_item
        except SQLAlchemyError as e:
            CartDatabase.rollback_transaction()
            print(f"Error updating cart item: {e}")
            raise ValueError("Error occurred while updating cart item.")

    @staticmethod
    def commit_transaction():
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            CartDatabase.rollback_transaction()
            print(f"Transaction commit failed: {e}")
            raise ValueError("Failed to commit transaction.")
        
    @staticmethod
    def delete_cart_item(cart_item):
        try:
            db.session.delete(cart_item)
        except Exception as e:
            CartDatabase.rollback_transaction()
            print(f"Error deleting nutrition facts for food item ID {cart_item.id}: {e}")
            raise ValueError("Failed to delete nutrition facts.")
    
    @staticmethod
    def rollback_transaction():
        try:
            db.session.rollback()
        except Exception as e:
            print(f"Error rolling back transaction: {e}")
            raise ValueError("Failed to rollback transaction.")

