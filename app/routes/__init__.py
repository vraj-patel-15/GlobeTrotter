from app.routes.admin import admin_bp
from app.routes.auth import auth_bp
from app.routes.budget import budget_bp
from app.routes.community import community_bp
from app.routes.dashboard import dashboard_bp
from app.routes.itinerary import itinerary_bp
from app.routes.search import search_bp
from app.routes.trips import trips_bp

__all__ = [
    "auth_bp",
    "dashboard_bp",
    "trips_bp",
    "itinerary_bp",
    "search_bp",
    "budget_bp",
    "community_bp",
    "admin_bp",
]