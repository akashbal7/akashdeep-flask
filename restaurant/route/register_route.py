from flask import Blueprint, request, jsonify
from restaurant.services.address_service import AddressService
from restaurant.services.register_service import UserService
from restaurant.services.review_service import ReviewService
from restaurant import app
import logging

logger = logging.getLogger(__name__)
register_bp = Blueprint('register_controller', __name__)
review_bp = Blueprint('review_bp', __name__)

@register_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        logger.info(f"Received registration request for email: {data['email']}")
        

        # Call the service to handle registration logic
        result, status_code = UserService.register_user(data)

        return jsonify(result), status_code

    except Exception as e:
        logger.exception("Registration error")
        return jsonify({'error': 'Registration failed. Please try again.'}), 500
    
    
@register_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        logger.info(f"Received Login request for email: {data['email']}")

        result, status_code = UserService.login_user(data)

        return jsonify(result), status_code

    except Exception as e:
        logger.exception("Login error")
        return jsonify({'error': 'Login failed. Please try again.'}), 500
    

@register_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        # Call the service to get the user data
        user_data, status_code = UserService.get_user_by_id(user_id)

        if status_code == 404:
            return jsonify({'error': 'User not found.'}), 404

        return jsonify(user_data), status_code

    except Exception as e:
        logger.exception("Error retrieving user by ID")
        return jsonify({'error': 'Failed to retrieve user. Please try again later.'}), 500
    
@register_bp.route('/user/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    try:
        data = request.get_json()
        logger.info(f"Received edit request for user ID: {user_id}")

        result, status_code = UserService.edit_user(user_id, data)

        if status_code == 404:
            return jsonify({'error': 'User not found.'}), 404

        return jsonify(result), status_code

    except Exception as e:
        logger.exception("Error editing user")
        return jsonify({'error': 'Failed to update user. Please try again later.'}), 500
    
@register_bp.route('/user/<int:user_id>/address/<int:address_id>', methods=['PUT'])
def edit_address(user_id,address_id):
    try:
        data = request.get_json()
        logger.info(f"Received address update request for user ID: {user_id}, address ID: {address_id}")

        result, status_code = AddressService.update_address(address_id, data)

        return jsonify(result), status_code

    except Exception as e:
        logger.exception("Error updating address")
        return jsonify({'error': 'Failed to update address. Please try again later.'}), 500

@review_bp.route('/reviews/<int:restaurant_id>', methods=['GET'])
def get_reviews(restaurant_id):
    reviews = ReviewService.get_reviews(restaurant_id)
    review_data = [
        {
            'food_rating': r.food_rating,
            'service_rating': r.service_rating,
            'value_rating': r.value_rating,
            'atmosphere_rating': r.atmosphere_rating,
            'review_text': r.review_text,
            'timestamp': r.timestamp  # Assuming timestamp is a field in Review model
        } for r in reviews
    ]
    return jsonify({'reviews': review_data}), 200

@review_bp.route('/reviews/<int:restaurant_id>', methods=['POST'])
def add_review(restaurant_id):
    data = request.json
    review = ReviewService.add_review(
        restaurant_id=restaurant_id,
        food=data['food_rating'],
        service=data['service_rating'],
        value=data['value_rating'],
        atmosphere=data['atmosphere_rating'],
        review_text=data.get('review_text', '')
    )
    return jsonify({'message': 'Review added successfully', 'review_id': review.id}), 201

