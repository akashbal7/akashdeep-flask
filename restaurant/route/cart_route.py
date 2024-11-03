from flask import Blueprint, request, jsonify
from restaurant.services.cart_service import CartService
import logging

logger = logging.getLogger(__name__)
cart_bp = Blueprint('cart_controller', __name__)

@cart_bp.route('/user/<int:user_id>/cart', methods=['POST'])
def add_food_into_cart(user_id):
    data = request.get_json()
    food_item_id = data.get('food_item_id')
    quantity = data.get('quantity')

    if not all([user_id, food_item_id, quantity]):
        return jsonify({"message": "Missing required parameters"}), 400

    try:
        cart_item = CartService.add_item_to_cart(user_id, food_item_id, quantity)
        return jsonify(cart_item), 201

    except ValueError as e:
        return jsonify({"message": str(e)}), 500
    
@cart_bp.route('/user/<int:user_id>/cart/<int:cart_id>', methods=['PUT'])
def remove_cart_item_quantity(user_id, cart_id):
    try:
        cart_item, status = CartService.remove_item_quantity(user_id, cart_id)
        return jsonify(cart_item), status
    except Exception as e:
        return jsonify({"message": "Failed to update cart item quantity.", "error": str(e)}), 500
    
@cart_bp.route('/user/<int:user_id>/cart/<int:cart_id>', methods=['DELETE'])
def delete_cart_item(user_id, cart_id):
    try:
        cart_item, status = CartService.delete_cart_item(user_id, cart_id)
        return jsonify(cart_item), status
    except Exception as e:
        return jsonify({"message": "Failed to delete cart item.", "error": str(e)}), 500
    
@cart_bp.route('/user/<int:user_id>/cart', methods=['GET'])
def get_cart_items(user_id):
    try:
        cart_items, status = CartService.get_cart_items_by_user(user_id)
        return jsonify(cart_items), status
    except Exception as e:
        return jsonify({"message": "Failed to retrieve cart items.", "error": str(e)}), 500
    
