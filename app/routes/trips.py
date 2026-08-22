from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models.trip import Trip

trips_bp = Blueprint('trips', __name__, url_prefix='/trips')


@trips_bp.route('/')
@trips_bp.route('/list')
@login_required
def list_trips():
    user_trips = Trip.query.filter_by(user_id=current_user.id) \
        .order_by(Trip.start_date.desc()) \
        .all()

    return render_template('trips/list.html', trips=user_trips)


@trips_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Renders trip creation form and handles new trip creation."""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        start_date_str = request.form.get('start_date', '').strip()
        end_date_str = request.form.get('end_date', '').strip()
        budget = request.form.get('budget', type=float, default=0.0)
        is_public = True if request.form.get('is_public') else False

        if not title or not start_date_str or not end_date_str:
            flash('Title, start date, and end date are required.', 'danger')
            return render_template('trips/create.html', is_edit=False)

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')
            return render_template('trips/create.html', is_edit=False)

        if start_date > end_date:
            flash('End date must be on or after the start date.', 'danger')
            return render_template('trips/create.html', is_edit=False)

        new_trip = Trip(
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
            budget=budget,
            is_public=is_public,
            user_id=current_user.id
        )

        try:
            db.session.add(new_trip)
            db.session.commit()
            flash('Trip created successfully! You can now add cities and activities.', 'success')
            return redirect(url_for('itinerary.builder', trip_id=new_trip.id))
        except Exception:
            db.session.rollback()
            flash('An error occurred while creating the trip. Please try again.', 'danger')

    return render_template('trips/create.html', is_edit=False)


@trips_bp.route('/<int:trip_id>')
@login_required
def detail(trip_id):
    """Shows the summary details of a specific trip."""
    trip = Trip.query.get_or_404(trip_id)

    if trip.user_id != current_user.id and not trip.is_public:
        abort(403)

    return render_template('trips/detail.html', trip=trip)


@trips_bp.route('/<int:trip_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(trip_id):
    """Edits basic metadata of an existing trip."""
    trip = Trip.query.get_or_404(trip_id)

    if trip.user_id != current_user.id:
        abort(403)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        start_date_str = request.form.get('start_date', '').strip()
        end_date_str = request.form.get('end_date', '').strip()
        budget = request.form.get('budget', type=float, default=0.0)
        is_public = True if request.form.get('is_public') else False

        if not title or not start_date_str or not end_date_str:
            flash('Title, start date, and end date are required.', 'danger')
            return render_template('trips/create.html', trip=trip, is_edit=True)

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format.', 'danger')
            return render_template('trips/create.html', trip=trip, is_edit=True)

        if start_date > end_date:
            flash('End date must be on or after start date.', 'danger')
            return render_template('trips/create.html', trip=trip, is_edit=True)

        trip.title = title
        trip.description = description
        trip.start_date = start_date
        trip.end_date = end_date
        trip.budget = budget
        trip.is_public = is_public

        try:
            db.session.commit()
            flash('Trip updated successfully!', 'success')
            return redirect(url_for('trips.detail', trip_id=trip.id))
        except Exception:
            db.session.rollback()
            flash('Failed to update trip.', 'danger')

    return render_template('trips/create.html', trip=trip, is_edit=True)


@trips_bp.route('/<int:trip_id>/delete', methods=['POST'])
@login_required
def delete(trip_id):
    """Deletes a trip and associated items."""
    trip = Trip.query.get_or_404(trip_id)

    if trip.user_id != current_user.id:
        abort(403)

    try:
        db.session.delete(trip)
        db.session.commit()
        flash('Trip deleted successfully.', 'info')
    except Exception:
        db.session.rollback()
        flash('An error occurred while deleting the trip.', 'danger')

    return redirect(url_for('trips.list_trips'))