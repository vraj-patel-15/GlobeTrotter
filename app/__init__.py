import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app.config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with app context
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Configure Flask-Login settings
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "info"

    # User loader callback for Flask-Login
    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.trips import trips_bp
    from app.routes.itinerary import itinerary_bp
    from app.routes.search import search_bp
    from app.routes.budget import budget_bp
    from app.routes.community import community_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(trips_bp, url_prefix="/trips")
    app.register_blueprint(itinerary_bp, url_prefix="/itinerary")
    app.register_blueprint(search_bp, url_prefix="/search")
    app.register_blueprint(budget_bp, url_prefix="/budget")
    app.register_blueprint(community_bp, url_prefix="/community")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # Global error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template("500.html"), 500

    return app