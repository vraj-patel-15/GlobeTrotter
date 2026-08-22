from flask import Blueprint, render_template, request, jsonify
from app.models.city import City
from app.models.activity import Activity

search_bp = Blueprint('search', __name__, url_prefix='/search')


@search_bp.route('/cities', methods=['GET'])
def cities():
    """Renders the city search page and processes filtering queries."""
    query = request.args.get('q', '').strip()
    country_filter = request.args.get('country', '').strip()
    min_cost = request.args.get('min_cost', type=float)
    max_cost = request.args.get('max_cost', type=float)

    cities_query = City.query

    if query:
        cities_query = cities_query.filter(
            (City.name.ilike(f'%{query}%')) | (City.country.ilike(f'%{query}%'))
        )

    if country_filter:
        cities_query = cities_query.filter(City.country.ilike(f'%{country_filter}%'))

    if min_cost is not None and hasattr(City, 'cost_index'):
        cities_query = cities_query.filter(City.cost_index >= min_cost)

    if max_cost is not None and hasattr(City, 'cost_index'):
        cities_query = cities_query.filter(City.cost_index <= max_cost)

    results = cities_query.all()

    # Get distinct countries for filter dropdown
    countries = [c[0] for c in City.query.with_entities(City.country).distinct().all() if c[0]]

    # Return JSON response if requested via AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify([{
            'id': c.id,
            'name': c.name,
            'country': c.country,
            'description': getattr(c, 'description', ''),
            'cost_index': getattr(c, 'cost_index', None),
            'image_url': getattr(c, 'image_url', '')
        } for c in results])

    return render_template('search/cities.html', cities=results, countries=countries, query=query)


@search_bp.route('/activities', methods=['GET'])
def activities():
    """Renders the activity search page and processes category/cost filters."""
    query = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()
    city_id = request.args.get('city_id', type=int)
    max_cost = request.args.get('max_cost', type=float)

    activities_query = Activity.query

    if query:
        activities_query = activities_query.filter(
            (Activity.title.ilike(f'%{query}%')) | (Activity.description.ilike(f'%{query}%'))
        )

    if category:
        activities_query = activities_query.filter(Activity.category == category)

    if city_id:
        activities_query = activities_query.filter(Activity.city_id == city_id)

    if max_cost is not None:
        activities_query = activities_query.filter(Activity.estimated_cost <= max_cost)

    results = activities_query.all()

    # Distinct categories for sidebar filters
    categories = [cat[0] for cat in Activity.query.with_entities(Activity.category).distinct().all() if cat[0]]

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify([{
            'id': a.id,
            'title': a.title,
            'category': getattr(a, 'category', 'General'),
            'estimated_cost': getattr(a, 'estimated_cost', 0.0),
            'duration_hours': getattr(a, 'duration_hours', 1.0),
            'city_id': a.city_id
        } for a in results])

    return render_template('search/activities.html', activities=results, categories=categories, query=query)