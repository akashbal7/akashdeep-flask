from flask import Blueprint, request, jsonify
from restaurant.services.food_service import FoodService
from restaurant import app
import logging

logger = logging.getLogger(__name__)
review_bp = Blueprint('review', __name__)



    

