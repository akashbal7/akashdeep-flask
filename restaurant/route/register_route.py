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


@review_bp.route('/restaurant/<int:restaurant_id>/review', methods=['GET'])
def get_reviews(restaurant_id):
    reviews = ReviewService.get_reviews(restaurant_id)
    review_data = [
        {
            'rating': r.rating,
            'review_text': r.review_text
        } for r in reviews
    ]
    return jsonify({'reviews': review_data}), 200

@review_bp.route('/restaurant/<int:restaurant_id>/review', methods=['POST'])
def add_review(restaurant_id):
    data = request.json
    review = ReviewService.add_review(
        restaurant_id=restaurant_id,
        rating=data['rating'],
        review_text=data.get('review_text', '')
    )
    return jsonify({'message': 'Review added successfully', 'review_id': review.id}), 201

@review_bp.route('/food/<int:food_item_id>/review', methods=['POST'])
def add_food_reviews(food_item_id):
    data=request.json
    required_fields = ['rating', 'taste_rating', 'texture_rating', 'quality_rating', 'presentation_rating']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({'error': f'Missing fields: {", ".join(missing_fields)}'}), 400
    
    review = ReviewService.add_food_reviews(
        food_item_id=food_item_id,
        rating=data['rating'],
        taste_rating=data['taste_rating'],
        texture_rating=data['texture_rating'],
        quality_rating=data['quality_rating'],
        presentation_rating=data['presentation_rating'],
        review_text=data.get('review_text', '')
    )
    return jsonify({'message': 'Food review added successfully', 'review_id': review.id}), 201

@review_bp.route('/food/<int:food_item_id>/review', methods=['GET'])
def get_food_reviews(food_item_id):
    # Fetch reviews for the specified food item ID
    reviews = ReviewService.get_food_reviews(food_item_id)

    # If no reviews are found, return a 404 response
    if not reviews:
        return jsonify({'message': 'No reviews found for this food item'}), 404

    # Format reviews for JSON response
    review_list = [
        {
            'review_id': review.id,
            'rating': review.rating,
            'taste_rating': review.taste_rating,
            'texture_rating': review.texture_rating,
            'quality_rating': review.quality_rating,
            'presentation_rating': review.presentation_rating,
            'review_text': review.review_text,
            'created_at': review.created_at.isoformat()  # Assumes you have a timestamp field
        } for review in reviews
    ]

    return jsonify({'reviews': review_list}), 200