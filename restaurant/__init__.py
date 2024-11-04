from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS
import os

# Initialize Flask app
app = Flask(__name__)


# Load configuration from config.py
app.config.from_pyfile('../config.py')

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
migrate = Migrate(app, db)
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Make sure this folder exists
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is a secret'
print(SECRET_KEY)
app.config['SECRET_KEY'] = SECRET_KEY

# Import User model after app initialization to avoid circular import issues
@login_manager.user_loader
def load_user(user_id):
    from restaurant.model.models import User  # Import User here to prevent circular import
    return User.query.get(int(user_id))

# Allow CORS to enable communication between React (frontend) and Flask (backend)
CORS(app, 
     resources={r"/*": {
         "origins": ["http://localhost:5173"],
         "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         "allow_headers": ["Content-Type", "Authorization"],
         "supports_credentials": True
     }})

# Register blueprints function
def register_blueprints(app):
    # Import each route blueprint and register it
    from restaurant.route.register_route import register_bp
    from restaurant.route.food_route import food_bp
    from restaurant.route.restaurant_route import restaurant_bp
    from restaurant.route.cart_route import cart_bp
    from restaurant.route.review_route import review_bp
    
    app.register_blueprint(register_bp)
    app.register_blueprint(food_bp)
    app.register_blueprint(restaurant_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(review_bp)

# Register all blueprints
register_blueprints(app)
