from flask import Blueprint, request, jsonify
from restaurant.services.register_service import UserService
from restaurant import app
import logging

logger = logging.getLogger(__name__)
register_bp = Blueprint('register_controller', __name__)

@register_bp.route('/api/register', methods=['POST'])
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
