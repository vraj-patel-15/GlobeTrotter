from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, abort
from flask_login import login_required, current_user
from app import db
from app.models.trip import Trip
from app.models.expense import Expense
from app.services.budget_service import calculate_trip_budget

budget_bp = Blueprint('budget', __name__, url_prefix='/budget')


@budget_bp.route('/<int:trip_id>', methods=['GET'])
@login_required
def view_budget(trip_id):
    """Renders the detailed budget breakdown and expense manager for a trip."""
    trip = Trip.query.get_or_404(trip_id)

    if trip.user_id != current_user.id and not trip.is_public:
        abort(403)

    # Use service layer to compute dynamic breakdown and status
    budget_data = calculate_trip_budget(trip.id)
    expenses = Expense.query.filter_by(trip_id=trip.id).order_by(Expense.date.desc()).all()

    return render_template(
        'budget/budget.html',
        trip=trip,
        budget_data=budget_data,
        expenses=expenses
    )


@budget_bp.route('/<int:trip_id>/add-expense', methods=['POST'])
@login_required
def add_expense(trip_id):
    """Adds a new expense item to the specified trip."""
    trip = Trip.query.get_or_404(trip_id)

    if trip.user_id != current_user.id:
        abort(403)

    title = request.form.get('title', '').strip()
    amount = request.form.get('amount', type=float)
    category = request.form.get('category', 'General').strip()
    date_str = request.form.get('date', '').strip()

    if not title or amount is None or amount <= 0:
        flash('Please provide a valid title and positive amount for the expense.', 'danger')
        return redirect(url_for('budget.view_budget', trip_id=trip.id))

    new_expense = Expense(
        trip_id=trip.id,
        title=title,
        amount=amount,
        category=category,
        date=date_str if date_str else None
    )

    try:
        db.session.add(new_expense)
        db.session.commit()
        flash('Expense recorded successfully.', 'success')
    except Exception:
        db.session.rollback()
        flash('An error occurred while logging the expense.', 'danger')

    return redirect(url_for('budget.view_budget', trip_id=trip.id))


@budget_bp.route('/expense/<int:expense_id>/delete', methods=['POST'])
@login_required
def delete_expense(expense_id):
    """Deletes an expense item."""
    expense = Expense.query.get_or_404(expense_id)
    trip = Trip.query.get_or_404(expense.trip_id)

    if trip.user_id != current_user.id:
        abort(403)

    try:
        db.session.delete(expense)
        db.session.commit()
        flash('Expense deleted.', 'info')
    except Exception:
        db.session.rollback()
        flash('Failed to delete expense.', 'danger')

    return redirect(url_for('budget.view_budget', trip_id=trip.id))