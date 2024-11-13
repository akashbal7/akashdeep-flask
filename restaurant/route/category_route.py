from flask import Blueprint, request, jsonify
from restaurant.auth_middleware import token_required
from restaurant.database.category_database import CategoryDatabase
from restaurant.services.category_service import CategoryService
import logging


logger = logging.getLogger(__name__)
category_bp = Blueprint('category_controller', __name__)

@category_bp.route('/restaurant/<int:restaurant_id>/category', methods=['POST'])
def add_category(restaurant_id):
    data = request.get_json()
    category_name = data['name']
    
    category = CategoryDatabase.get_category_by_name(category_name)
    
    if category:
        success = CategoryService.link_category_to_restaurant(restaurant_id, category)
        if success:
            return jsonify({"message": "Category linked to restaurant.", "category_id": category.id}), 201
        else:
            return jsonify({"message": "Category already added to this restaurant.", "category_id": category.id}), 200
    else:
        try:
            new_category = CategoryService.add_category(data, restaurant_id)
            return new_category
        except Exception as e:
            return jsonify({"message": "Failed to add category.", "error": str(e)}), 500

@category_bp.route('/restaurant/<int:restaurant_id>/categories', methods=['GET'])
def get_categories(restaurant_id):
    try:
        categories = CategoryService.get_categories_by_restaurant(restaurant_id)
        category_list = [category.to_dict() for category in categories]
        return jsonify({"data": category_list}), 200
    except Exception as e:
        return jsonify({"message": "Failed to retrieve categories.", "error": str(e)}), 500
    
@category_bp.route('/categories', methods=['GET'])
def get_all_categories():
    try:
        categories = CategoryService.get_all_categories()
        category_list = [category.to_dict() for category in categories]
        return jsonify({"categories": category_list}), 200
    except Exception as e:
        return jsonify({"message": "Failed to retrieve categories.", "error": str(e)}), 500