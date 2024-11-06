from flask import Blueprint, request, jsonify
from restaurant.model.models import User
from restaurant.services.register_service import UserService
from restaurant import app
import jwt
import os
import logging
from ..validate import validate_email_and_password


logger = logging.getLogger(__name__)
register_bp = Blueprint('register_controller', __name__)

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
        if not data:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
        logger.info(f"Received Login request for email: {data['email']}")
        
        is_validated = validate_email_and_password(data.get('email'), data.get('password'))
        if is_validated is not True:
            return dict(message='Invalid data', data=None, error=is_validated), 400
        
        user = UserService.login_user(data)

        logger.info(f"user: {user}")
        if user:
            try:
                # token should expire after 24 hrs
                user["token"] = jwt.encode(
                    {"id": user["id"], "email": user["email"]},
                    app.config["SECRET_KEY"],
                    algorithm="HS256"
                )
                return {
                    "message": "Successfully fetched auth token",
                    "data": user
                }
            except Exception as e:
                return {
                    "error": "Something went wrong",
                    "message": str(e)
                }, 500
        return {
            "message": "Invalid email or password",
            "data": None,
            "error": "Unauthorized"
        }, 404
    except Exception as e:
        logger.error(f"Error during login: {e}")
        return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": None
        }, 500
    

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



    

