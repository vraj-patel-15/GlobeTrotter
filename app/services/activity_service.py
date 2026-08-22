from typing import List, Optional, Dict, Any
from sqlalchemy import or_
from app import db
from app.models.activity import Activity


def get_activities_by_city(city_id: int) -> List[Activity]:
    """Retrieves all activities located in a specific city."""
    return Activity.query.filter_by(city_id=city_id).order_by(Activity.title.asc()).all()


def get_activity_by_id(activity_id: int) -> Optional[Activity]:
    """Retrieves a single activity by its primary key ID."""
    return Activity.query.get(activity_id)


def search_activities(
        query_str: Optional[str] = None,
        city_id: Optional[int] = None,
        category: Optional[str] = None,
        max_cost: Optional[float] = None,
        max_duration: Optional[float] = None
) -> List[Activity]:
    """
    Searches and filters activities based on user input criteria.
    """
    stmt = Activity.query

    if city_id:
        stmt = stmt.filter(Activity.city_id == city_id)

    if query_str and query_str.strip():
        search_term = f"%{query_str.strip()}%"
        stmt = stmt.filter(
            or_(
                Activity.title.ilike(search_term),
                Activity.description.ilike(search_term) if hasattr(Activity, 'description') else False
            )
        )

    if category and category.strip():
        stmt = stmt.filter(Activity.category.ilike(f"%{category.strip()}%"))

    if max_cost is not None and hasattr(Activity, 'estimated_cost'):
        stmt = stmt.filter(Activity.estimated_cost <= max_cost)

    if max_duration is not None and hasattr(Activity, 'duration_hours'):
        stmt = stmt.filter(Activity.duration_hours <= max_duration)

    return stmt.order_by(Activity.title.asc()).all()


def get_distinct_categories() -> List[str]:
    """Fetches all unique activity categories available in the database."""
    if hasattr(Activity, 'category'):
        results = db.session.query(Activity.category).distinct().order_by(Activity.category.asc()).all()
        return [r[0] for r in results if r[0]]
    return []


def calculate_activities_cost(activity_ids: List[int]) -> float:
    """Calculates total cost for a list of activity IDs."""
    if not activity_ids:
        return 0.0

    total = db.session.query(db.func.sum(Activity.estimated_cost)) \
        .filter(Activity.id.in_(activity_ids)) \
        .scalar()

    return float(total or 0.0)