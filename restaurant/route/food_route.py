from flask import Blueprint, request, jsonify
from restaurant.services.food_service import FoodService
from restaurant import app
import logging

logger = logging.getLogger(__name__)
food_bp = Blueprint('food', __name__)

@app.route('/restaurant/<int:restaurant_id>/food', methods=['POST'])
def add_food_item(restaurant_id):
    
    data = request.get_json()
    try:
        food_item = FoodService.add_food_item(data, restaurant_id)
        return jsonify({"message": "Food item added successfully.", "food_item_id": food_item.id}), 201
    except Exception as e:
        return jsonify({"message": "Failed to add food item.", "error": str(e)}), 500
    
@app.route('/restaurant/<int:restaurant_id>/food/<int:food_item_id>', methods=['GET'])
def get_food_item(restaurant_id, food_item_id):
    try:
        food_item = FoodService.get_food_item(restaurant_id, food_item_id)
        return jsonify(food_item), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
@app.route('/restaurant/<int:restaurant_id>/food/<int:food_item_id>', methods=['PUT'])
def update_food_item(restaurant_id, food_item_id):
    data = request.get_json()
    try:
        updated_food_item = FoodService.update_food_item(data, restaurant_id, food_item_id)
        return jsonify({"message": "Food item updated successfully.", "food_item": updated_food_item}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
@app.route('/restaurant/<int:restaurant_id>/food/<int:food_item_id>', methods=['DELETE'])
def delete_food_item(restaurant_id, food_item_id):
    try:
        FoodService.delete_food_item(restaurant_id, food_item_id)
        return jsonify({"message": "Food item deleted successfully."}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

    

