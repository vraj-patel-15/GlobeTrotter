from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, abort
from flask_login import login_required, current_user
from app import db
from app.models.trip import Trip
from app.models.city import City
from app.models.activity import Activity
from app.models.itinerary import ItineraryStop, ItineraryItem, Stop

itinerary_bp = Blueprint('itinerary', __name__, url_prefix='/itinerary')


@itinerary_bp.route('/builder/<int:trip_id>', methods=['GET'])
@login_required
def builder(trip_id):
    """Renders the interactive itinerary builder page."""
    trip = Trip.query.get_or_404(trip_id)
    if trip.user_id != current_user.id:
        abort(403)

    stops = Stop.query.filter_by(trip_id=trip_id).order_by(Stop.start_date.asc(), Stop.order_index.asc()).all()
    all_cities = City.query.order_by(City.name.asc()).all()

    return render_template('itinerary/builder.html', trip=trip, stops=stops, cities=all_cities)


@itinerary_bp.route('/view/<int:trip_id>', methods=['GET'])
def view(trip_id):
    """Renders the completed, structured itinerary view (accessible publicly if trip is public)."""
    trip = Trip.query.get_or_404(trip_id)
    if not trip.is_public and (not current_user.is_authenticated or trip.user_id != current_user.id):
        abort(403)

    stops = ItineraryStop.query.filter_by(trip_id=trip.id).order_by(ItineraryStop.arrival_date.asc()).all()

    # Calculate days list for day-wise itinerary rendering
    trip_days = []
    if trip.start_date and trip.end_date:
        current_date = trip.start_date
        day_num = 1
        while current_date <= trip.end_date:
            trip_days.append({'day_number': day_num, 'date': current_date})
            current_date += timedelta(days=1)
            day_num += 1

    return render_template('itinerary/view.html', trip=trip, stops=stops, trip_days=trip_days)


@itinerary_bp.route('/calendar/<int:trip_id>', methods=['GET'])
@login_required
def calendar(trip_id):
    """Renders the timeline/calendar view of the trip."""
    trip = Trip.query.get_or_404(trip_id)
    if trip.user_id != current_user.id and not trip.is_public:
        abort(403)

    stops = ItineraryStop.query.filter_by(trip_id=trip.id).order_by(ItineraryStop.arrival_date.asc()).all()
    return render_template('itinerary/calendar.html', trip=trip, stops=stops)


@itinerary_bp.route('/stop/add/<int:trip_id>', methods=['POST'])
@login_required
def add_stop(trip_id):
    """Adds a city stop to an existing trip."""
    trip = Trip.query.get_or_404(trip_id)
    if trip.user_id != current_user.id:
        abort(403)

    city_id = request.form.get('city_id', type=int)
    arrival_str = request.form.get('arrival_date', '').strip()
    departure_str = request.form.get('departure_date', '').strip()

    if not city_id or not arrival_str or not departure_str:
        flash('City, arrival, and departure dates are required.', 'danger')
        return redirect(url_for('itinerary.builder', trip_id=trip.id))

    try:
        arrival_date = datetime.strptime(arrival_str, '%Y-%m-%d').date()
        departure_date = datetime.strptime(departure_str, '%Y-%m-%d').date()
    except ValueError:
        flash('Invalid date format provided.', 'danger')
        return redirect(url_for('itinerary.builder', trip_id=trip.id))

    if arrival_date > departure_date:
        flash('Arrival date cannot be after departure date.', 'danger')
        return redirect(url_for('itinerary.builder', trip_id=trip.id))

    new_stop = ItineraryStop(
        trip_id=trip.id,
        city_id=city_id,
        arrival_date=arrival_date,
        departure_date=departure_date
    )

    try:
        db.session.add(new_stop)
        db.session.commit()
        flash('City stop added successfully!', 'success')
    except Exception:
        db.session.rollback()
        flash('An error occurred while adding the stop.', 'danger')

    return redirect(url_for('itinerary.builder', trip_id=trip.id))


@itinerary_bp.route('/stop/<int:stop_id>/delete', methods=['POST'])
@login_required
def delete_stop(stop_id):
    """Removes a city stop from a trip."""
    stop = ItineraryStop.query.get_or_404(stop_id)
    trip = Trip.query.get_or_404(stop.trip_id)
    if trip.user_id != current_user.id:
        abort(403)

    try:
        db.session.delete(stop)
        db.session.commit()
        flash('City stop removed.', 'info')
    except Exception:
        db.session.rollback()
        flash('Failed to remove stop.', 'danger')

    return redirect(url_for('itinerary.builder', trip_id=trip.id))


@itinerary_bp.route('/item/add/<int:stop_id>', methods=['POST'])
@login_required
def add_item(stop_id):
    """Adds an activity item to a specific stop."""
    stop = ItineraryStop.query.get_or_404(stop_id)
    trip = Trip.query.get_or_404(stop.trip_id)
    if trip.user_id != current_user.id:
        abort(403)

    activity_id = request.form.get('activity_id', type=int)
    day_number = request.form.get('day_number', type=int, default=1)
    notes = request.form.get('notes', '').strip()

    if not activity_id:
        flash('Please select an activity to add.', 'danger')
        return redirect(url_for('itinerary.builder', trip_id=trip.id))

    item = ItineraryItem(
        stop_id=stop.id,
        activity_id=activity_id,
        day_number=day_number,
        notes=notes
    )

    try:
        db.session.add(item)
        db.session.commit()
        flash('Activity added to itinerary!', 'success')
    except Exception:
        db.session.rollback()
        flash('Failed to add activity.', 'danger')

    return redirect(url_for('itinerary.builder', trip_id=trip.id))