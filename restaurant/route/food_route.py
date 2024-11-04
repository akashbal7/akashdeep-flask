from flask import Blueprint, request, jsonify
from restaurant.auth_middleware import token_required
from restaurant.services.food_service import FoodService
import logging

logger = logging.getLogger(__name__)
food_bp = Blueprint('food_controller', __name__)

@food_bp.route('/restaurant/<int:restaurant_id>/food', methods=['POST'])
def add_food_item(restaurant_id):
    data = request.form  # Use request.form for form data and file uploads
    image_file = request.files.get('image')
    data = request.get_json()
    try:
        food_item = FoodService.add_food_item(data, restaurant_id, image_file)
        return jsonify({"message": "Food item added successfully.", "food_item_id": food_item.id}), 201
    except Exception as e:
        return jsonify({"message": "Failed to add food item.", "error": str(e)}), 500
    
@food_bp.route('/restaurant/<int:restaurant_id>/food/<int:food_item_id>', methods=['GET'])
@token_required
def get_food_item(current_user, restaurant_id, food_item_id):
    try:
        food_item = FoodService.get_food_item(restaurant_id, food_item_id)
        return jsonify(food_item), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
@food_bp.route('/restaurant/<int:restaurant_id>/food/<int:food_item_id>', methods=['PUT'])
def update_food_item(restaurant_id, food_item_id):
    data = request.get_json()
    try:
        updated_food_item = FoodService.update_food_item(data, restaurant_id, food_item_id)
        return jsonify({"message": "Food item updated successfully.", "food_item": updated_food_item}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
@food_bp.route('/restaurant/<int:restaurant_id>/food/<int:food_item_id>', methods=['DELETE'])
def delete_food_item(restaurant_id, food_item_id):
    try:
        FoodService.delete_food_item(restaurant_id, food_item_id)
        return jsonify({"message": "Food item deleted successfully."}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
@food_bp.route('/restaurant/<int:restaurant_id>/foods', methods=['GET'])
@token_required
def get_food_list(current_user, restaurant_id):
    try:
        food_list = FoodService.get_restaurant_food_list(restaurant_id)
        return jsonify({"foods": food_list}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 500
    
@food_bp.route('/foods', methods=['GET'])
def get_all_foods():
    try:
        category = request.args.get('category')
        all_foods = FoodService.get_all_foods(category)
        return jsonify(all_foods), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 500
    
@food_bp.route('/food/<int:food_item_id>/nutrition', methods=['GET'])
def get_food_nutrition_fact(food_item_id):
    try:
        # Call service layer to get nutrition facts
        nutrition_fact = FoodService.get_food_nutrition_fact(food_item_id)
        return jsonify({"nutrition_fact": nutrition_fact}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 404
    except Exception as e:
        return jsonify({"message": "Failed to retrieve nutrition facts.", "error": str(e)}), 500



    

