from flask import Blueprint, request, jsonify
from restaurant.services.restaurant_service import RestaurantService
from restaurant.services.address_service import AddressService
from restaurant import app
import logging

logger = logging.getLogger(__name__)
restaurant_bp = Blueprint('restaurant_controller', __name__)

@restaurant_bp.route('/restaurant/<int:restaurant_id>', methods=['PUT'])
def update_restaurant(restaurant_id):
    data = request.get_json()
    try:
        updated_restaurant = RestaurantService.update_restaurant(data, restaurant_id)
        return jsonify({"message": "Restaurant updated successfully.", "restaurant_id": updated_restaurant.id}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 404
    except Exception as e:
        return jsonify({"message": "Failed to update restaurant.", "error": str(e)}), 500
    
@restaurant_bp.route('/restaurant/<int:restaurant_id>/address/<int:address_id>', methods=['PUT'])
def edit_address(restaurant_id, address_id):
    try:
        data = request.get_json()
        logger.info(f"Received address update request for user ID: {restaurant_id}, address ID: {address_id}")

        result, status_code = AddressService.update_address(address_id, data)

        return jsonify(result), status_code

    except Exception as e:
        logger.exception("Error updating address")
        return jsonify({'error': 'Failed to update address. Please try again later.'}), 500
