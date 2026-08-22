from typing import List, Optional, Dict, Any
from sqlalchemy import or_, func
from app import db
from app.models.city import City


def get_all_cities(limit: Optional[int] = None) -> List[City]:
    """Retrieves all cities, optionally limited by quantity."""
    query = City.query.order_by(City.name.asc())
    if limit:
        query = query.limit(limit)
    return query.all()


def get_city_by_id(city_id: int) -> Optional[City]:
    """Retrieves a single city by its primary key ID."""
    return City.query.get(city_id)


def search_cities(
        query_str: Optional[str] = None,
        country: Optional[str] = None,
        max_cost_index: Optional[float] = None,
        min_cost_index: Optional[float] = None
) -> List[City]:
    """
    Searches and filters cities based on search terms, country, and cost index range.
    """
    stmt = City.query

    if query_str:
        search_term = f"%{query_str.strip()}%"
        stmt = stmt.filter(
            or_(
                City.name.ilike(search_term),
                City.country.ilike(search_term),
                City.description.ilike(search_term) if hasattr(City, 'description') else False
            )
        )

    if country and country.strip():
        stmt = stmt.filter(City.country.ilike(f"%{country.strip()}%"))

    if max_cost_index is not None and hasattr(City, 'cost_index'):
        stmt = stmt.filter(City.cost_index <= max_cost_index)

    if min_cost_index is not None and hasattr(City, 'cost_index'):
        stmt = stmt.filter(City.cost_index >= min_cost_index)

    return stmt.order_by(City.name.asc()).all()


def get_popular_cities(limit: int = 6) -> List[City]:
    """Fetches top popular cities ordered by popularity score or activity count."""
    if hasattr(City, 'popularity_score'):
        return City.query.order_by(City.popularity_score.desc()).limit(limit).all()

    return City.query.order_by(City.id.asc()).limit(limit).all()


def get_distinct_countries() -> List[str]:
    """Returns a list of all unique countries available in the database."""
    results = db.session.query(City.country).distinct().order_by(City.country.asc()).all()
    return [r[0] for r in results if r[0]]


def calculate_city_estimated_cost(city_id: int, num_days: int = 1) -> Dict[str, Any]:
    """
    Calculates estimated cost for staying in a city based on daily cost index and activity averages.
    """
    city = get_city_by_id(city_id)
    if not city:
        return {'daily_cost': 0.0, 'total_estimated_cost': 0.0, 'city_id': city_id}

    cost_index = getattr(city, 'cost_index', 50.0) or 50.0
    # Standard base daily cost formula using cost index
    daily_base_cost = cost_index * 1.5
    total_cost = daily_base_cost * num_days

    return {
        'city_id': city.id,
        'city_name': city.name,
        'country': city.country,
        'daily_cost': round(daily_base_cost, 2),
        'num_days': num_days,
        'total_estimated_cost': round(total_cost, 2)
    }