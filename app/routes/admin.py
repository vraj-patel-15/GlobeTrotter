from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.trip import Trip
from app.models.city import City
from app.models.activity import Activity
from sqlalchemy import func

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    """Decorator to enforce admin access privileges."""
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not getattr(current_user, 'is_admin', False):
            flash('Access denied. Administrator rights required.', 'danger')
            return redirect(url_for('dashboard.home'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function


@admin_bp.route('/dashboard', methods=['GET'])
@login_required
@admin_required
def dashboard():
    """Renders the admin analytics dashboard with platform usage statistics."""
    total_users = User.query.count()
    total_trips = Trip.query.count()
    public_trips_count = Trip.query.filter_by(is_public=True).count()
    total_cities = City.query.count()
    total_activities = Activity.query.count()

    # Most recent registered users
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()

    # Most recent trips
    recent_trips = Trip.query.order_by(Trip.created_at.desc()).limit(5).all()

    # Aggregate metric: Top popular cities based on recommendations/popularity
    popular_cities = City.query.order_by(
        City.popularity_score.desc() if hasattr(City, 'popularity_score') else City.id.asc()
    ).limit(5).all()

    stats = {
        'total_users': total_users,
        'total_trips': total_trips,
        'public_trips_count': public_trips_count,
        'total_cities': total_cities,
        'total_activities': total_activities
    }

    return render_template(
        'admin/dashboard.html',
        stats=stats,
        recent_users=recent_users,
        recent_trips=recent_trips,
        popular_cities=popular_cities
    )


@admin_bp.route('/users/toggle-admin/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def toggle_admin(user_id):
    """Grants or revokes admin privileges for a given user."""
    if user_id == current_user.id:
        flash('You cannot alter your own administrator status.', 'warning')
        return redirect(url_for('admin.dashboard'))

    user = User.query.get_or_404(user_id)
    if hasattr(user, 'is_admin'):
        user.is_admin = not user.is_admin
        try:
            db.session.commit()
            status = "granted" if user.is_admin else "revoked"
            flash(f'Admin status {status} for {user.username}.', 'success')
        except Exception:
            db.session.rollback()
            flash('Failed to update user privileges.', 'danger')

    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """Deletes a user account and associated data."""
    if user_id == current_user.id:
        flash('You cannot delete your own admin account.', 'warning')
        return redirect(url_for('admin.dashboard'))

    user = User.query.get_or_404(user_id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash(f'User {user.username} deleted.', 'info')
    except Exception:
        db.session.rollback()
        flash('Failed to delete user.', 'danger')

    return redirect(url_for('admin.dashboard'))