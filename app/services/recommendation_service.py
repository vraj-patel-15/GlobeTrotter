from typing import List, Dict, Any
from app.models.city import City
from app.models.activity import Activity
from app.models.trip import Trip


def recommend_cities_for_trip(
    budget: float = 0.0,
    duration_days: int = 1,
    limit: int = 5
) -> List[City]:
    """
    Recommends top cities based on daily budget allowance and popularity score.
    """
    cities_query = City.query

    # If a budget is provided, calculate target max cost index
    if budget > 0 and duration_days > 0:
        daily_budget = budget / duration_days
        # Map daily budget to estimated cost index scale
        max_cost_index = min(daily_budget / 1.5, 100.0)
        if hasattr(City, 'cost_index'):
            cities_query = cities_query.filter(City.cost_index <= max_cost_index)

    if hasattr(City, 'popularity_score'):
        cities_query = cities_query.order_by(City.popularity_score.desc())
    else:
        cities_query = cities_query.order_by(City.id.asc())

    return cities_query.limit(limit).all()


def recommend_activities_for_city(
    city_id: int,
    max_budget: float = 0.0,
    category: str = None,
    limit: int = 6
) -> List[Activity]:
    """
    Recommends activities for a specific city matching budget constraints and optional category preferences.
    """
    query = Activity.query.filter_by(city_id=city_id)

    if max_budget > 0 and hasattr(Activity, 'estimated_cost'):
        query = query.filter(Activity.estimated_cost <= max_budget)

    if category and hasattr(Activity, 'category'):
        query = query.filter(Activity.category.ilike(f"%{category.strip()}%"))

    return query.order_by(
        Activity.estimated_cost.asc() if hasattr(Activity, 'estimated_cost') else Activity.id.asc()
    ).limit(limit).all()


def get_personalized_recommendations(user_id: int, limit: int = 4) -> List[City]:
    """
    Generates personalized destination recommendations based on a user's past trip history and preferences.
    """
    # Fetch cities the user has already visited in past trips
    visited_city_ids = []
    user_trips = Trip.query.filter_by(user_id=user_id).all()
    for trip in user_trips:
        for stop in trip.stops:
            visited_city_ids.append(stop.city_id)

    # Recommend top popular cities excluding those already added
    query = City.query
    if visited_city_ids:
        query = query.filter(~City.id.in_(visited_city_ids))

    if hasattr(City, 'popularity_score'):
        query = query.order_by(City.popularity_score.desc())
    else:
        query = query.order_by(City.id.asc())

    return query.limit(limit).all()