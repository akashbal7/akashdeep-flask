from flask import Blueprint, request, jsonify
from restaurant.services.review_service import ReviewService
import logging

logger = logging.getLogger(__name__)
review_bp = Blueprint('review_controller', __name__)

@review_bp.route('/restaurant/<int:restaurant_id>/review', methods=['POST'])
def add_restaurant_review(restaurant_id):
    data = request.get_json()
    customer_id = data.get('customer_id')  # Assumed to be passed in the JSON body

    # Call the service layer to add the review
    response, status_code = ReviewService.add_review(data, customer_id, restaurant_id)
    
    return jsonify(response), status_code

@review_bp.route('/restaurant/<int:restaurant_id>/reviews', methods=['GET'])
def get_restaurant_reviews(restaurant_id):
    response, status_code = ReviewService.get_restaurant_reviews(restaurant_id)
    return jsonify(response), status_code

@review_bp.route('/food/<int:food_item_id>/review', methods=['POST'])
def add_food_review(food_item_id):
    data = request.get_json()
    customer_id = data.get("customer_id")  # Assumes customer_id is provided in the JSON request
    response, status_code = ReviewService.add_food_review(data, customer_id, food_item_id)
    return jsonify(response), status_code

@review_bp.route('/food/<int:food_item_id>/reviews', methods=['GET'])
def get_food_reviews(food_item_id):
    response, status_code = ReviewService.get_food_reviews(food_item_id)
    return jsonify(response), status_code
    

    
