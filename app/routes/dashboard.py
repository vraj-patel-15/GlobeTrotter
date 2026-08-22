from datetime import datetime
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.trip import Trip
from app.models.city import City
from app.models.expense import Expense
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def home():
    """Renders the main user dashboard with trip summaries, stats, and recommendations."""
    # Retrieve user's upcoming and active trips
    user_trips = Trip.query.filter_by(user_id=current_user.id) \
        .order_by(Trip.start_date.asc()) \
        .all()

    # Separate upcoming/active trips from past trips
    today = datetime.now().date()
    upcoming_trips = [t for t in user_trips if t.end_date >= today]
    recent_trips = user_trips[:3]  # Show top 3 most relevant/recent trips

    # Calculate aggregate dashboard metrics
    total_trips_count = len(user_trips)

    # Calculate overall user expenditure across all trips
    total_spent = Expense.query.join(Trip) \
                      .filter(Trip.user_id == current_user.id) \
                      .with_entities(func.sum(Expense.amount)) \
                      .scalar() or 0.0

    # Fetch featured / recommended popular destinations for inspiration
    recommended_cities = City.query.order_by(
        City.popularity_score.desc() if hasattr(City, 'popularity_score') else City.id.asc()).limit(4).all()

    # Community highlighted public trips
    community_trips = Trip.query.filter(Trip.is_public == True, Trip.user_id != current_user.id) \
        .order_by(Trip.created_at.desc()) \
        .limit(3) \
        .all()

    return render_template(
        'dashboard/home.html',
        user=current_user,
        recent_trips=recent_trips,
        upcoming_trips=upcoming_trips,
        total_trips_count=total_trips_count,
        total_spent=round(total_spent, 2),
        recommended_cities=recommended_cities,
        community_trips=community_trips
    )