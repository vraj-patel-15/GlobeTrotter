from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models.trip import Trip
from app.models.itinerary import ItineraryStop, ItineraryItem

community_bp = Blueprint('community', __name__, url_prefix='/community')


@community_bp.route('/', methods=['GET'])
def index():
    """Renders the public community hub with shared itineraries."""
    query = request.args.get('q', '').strip()

    public_trips_query = Trip.query.filter_by(is_public=True)

    if query:
        public_trips_query = public_trips_query.filter(
            (Trip.title.ilike(f'%{query}%')) | (Trip.description.ilike(f'%{query}%'))
        )

    public_trips = public_trips_query.order_by(Trip.created_at.desc()).all()

    return render_template('community/community.html', trips=public_trips, query=query)


@community_bp.route('/trip/<int:trip_id>', methods=['GET'])
def view_public_trip(trip_id):
    """Renders a public read-only view of a shared itinerary."""
    trip = Trip.query.get_or_404(trip_id)

    if not trip.is_public:
        flash('This trip is private and cannot be viewed.', 'warning')
        return redirect(url_for('community.index'))

    stops = ItineraryStop.query.filter_by(trip_id=trip.id).order_by(ItineraryStop.arrival_date.asc()).all()

    return render_template('itinerary/view.html', trip=trip, stops=stops, is_public_view=True)


@community_bp.route('/copy/<int:trip_id>', methods=['POST'])
@login_required
def clone_trip(trip_id):
    """Clones/copies a public trip into the logged-in user's personal account."""
    source_trip = Trip.query.get_or_404(trip_id)

    if not source_trip.is_public and source_trip.user_id != current_user.id:
        abort(403)

    # Create duplicate trip entity for current user
    new_trip = Trip(
        title=f"Copy of {source_trip.title}",
        description=source_trip.description,
        start_date=source_trip.start_date,
        end_date=source_trip.end_date,
        budget=source_trip.budget,
        is_public=False,
        user_id=current_user.id
    )

    try:
        db.session.add(new_trip)
        db.session.flush()  # Generate ID for new_trip

        # Deep clone stops and associated itinerary items
        for old_stop in source_trip.stops:
            new_stop = ItineraryStop(
                trip_id=new_trip.id,
                city_id=old_stop.city_id,
                arrival_date=old_stop.arrival_date,
                departure_date=old_stop.departure_date
            )
            db.session.add(new_stop)
            db.session.flush()

            for old_item in old_stop.items:
                new_item = ItineraryItem(
                    stop_id=new_stop.id,
                    activity_id=old_item.activity_id,
                    day_number=old_item.day_number,
                    notes=old_item.notes
                )
                db.session.add(new_item)

        db.session.commit()
        flash('Trip successfully copied to your account! You can now customize it.', 'success')
        return redirect(url_for('itinerary.builder', trip_id=new_trip.id))

    except Exception:
        db.session.rollback()
        flash('An error occurred while copying the trip.', 'danger')
        return redirect(url_for('community.index'))