from restaurant.database.cart_database import CartDatabase
import logging, base64
from flask import current_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CartService:
        
    @staticmethod
    def add_item_to_cart(customer_id, food_item_id, quantity):
        try:
            cart_item = CartDatabase.get_cart_item(customer_id, food_item_id)
            
            if cart_item:
                # Update the quantity if the cart item already exists
                cart_item.quantity += quantity
                CartDatabase.update_cart_item(cart_item)
            else:
                # Create and add a new cart item
                cart_item = CartDatabase.add_cart_item(customer_id, food_item_id, quantity)

            CartDatabase.commit_transaction()
            return {
            "message": "Food item added to cart successfully.",
            "data": {
                "id": cart_item.id,
                "customer_id": cart_item.customer_id,
                "food_item_id": cart_item.food_item_id,
                "quantity": cart_item.quantity
            }
        }

        except ValueError as e:
            print(f"Failed to add item to cart: {e}")
            raise ValueError("Uanble to add item into cart, try again")
        
    @staticmethod
    def update_item_quantity(data, customer_id, cart_id):
    # Retrieve the cart item
        if "quantity" not in data or not isinstance(data["quantity"], int) or data["quantity"] < 0:
            return {
                "message": "Invalid quantity provided.",
                "data": {"customer_id": customer_id}
            }, 400
        cart_item = CartDatabase.get_cart_by_id(cart_id)

        if not cart_item:
            return {
                "message": "Cart item not found.",
                "data": {
                    
                    "customer_id": customer_id
                }
            }, 404

        # Initialize the result variable
        result = {}

        # Check if quantity is greater than 1 before reducing
        if cart_item.quantity > 0:
            cart_item.quantity = data["quantity"]
            print("cart", cart_item)
            CartDatabase.update_cart_item(cart_item)  # Update the quantity in the database
            result = {
                "message": "Quantity updated successfully.",
                "data": {
                    "id": cart_item.id,
                    "customer_id": cart_item.customer_id,
                    "food_item_id": cart_item.food_item_id,
                    "quantity": cart_item.quantity
                }
            }
        else:
            # If quantity is 1, remove the cart item entirely
            CartDatabase.delete_cart_item(cart_item)  # Remove the cart item
            result = {
                "message": "Cart item removed.",
                "data": {
                    "id": cart_item.id,
                    "customer_id": cart_item.customer_id
                }
            }

        # Commit the transaction after either update or delete
        CartDatabase.commit_transaction()
        
        return result, 200
    
    @staticmethod
    def delete_cart_item(customer_id, cart_id):
    # Retrieve the cart item
        cart_item = CartDatabase.get_cart_by_id(cart_id)
        print("cartttttttt", cart_item)

        if not cart_item:
            return {
                "message": "Cart item not found.",
                "data": {
                    
                    "customer_id": customer_id
                }
            }, 404
            
        CartDatabase.delete_cart_item(cart_item) 

        # Commit the transaction after either update or delete
        CartDatabase.commit_transaction()
        
        return {
                "message": "Cart item deleted successfully.",
                "data": [],
            }, 200
        
    @staticmethod
    def get_cart_items_by_user(user_id):
        upload_folder = current_app.config['UPLOAD_FOLDER']
        # Retrieve all cart items for the specified user
        cart_items = CartDatabase.get_cart_items_by_user(user_id)

        if not cart_items:
             return {
                "message": "Cart item not found.",
                "data": []
            }, 404

        # Format the response data
        cart_items_array = []
        for item in cart_items:
            if item.food_item.image_filename:
                with open(f"{upload_folder}/{item.food_item.image_filename}", "rb") as img_file:
                    encoded_image = base64.b64encode(img_file.read()).decode('utf-8')
            else:
                encoded_image = None
            cart_items_array.append({
                    "id": item.id,
                    "food_item": {
                        **item.food_item.to_dict(),
                        "image_data": encoded_image
                    },
                    "quantity": item.quantity,
                    "added_at": item.created_at.isoformat(),
                })
        return {
                "message": "Cart items retrieved successfully.",
                "data": cart_items_array
            }, 200
        
         