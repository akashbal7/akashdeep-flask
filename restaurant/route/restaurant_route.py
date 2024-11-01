from flask import Blueprint, request, jsonify
from restaurant.services.restaurant_service import RestaurantService
from restaurant import app
import logging

logger = logging.getLogger(__name__)
restaurant_bp = Blueprint('restaurant_controller', __name__)

@app.route('/restaurant/<int:restaurant_id>', methods=['PUT'])
def update_restaurant(restaurant_id):
    data = request.get_json()
    try:
        updated_restaurant = RestaurantService.update_restaurant(data, restaurant_id)
        return jsonify({"message": "Restaurant updated successfully.", "restaurant_id": updated_restaurant.id}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 404
    except Exception as e:
        return jsonify({"message": "Failed to update restaurant.", "error": str(e)}), 500
