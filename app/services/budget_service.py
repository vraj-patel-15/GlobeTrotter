from typing import Dict, Any, List
from sqlalchemy import func
from app import db
from app.models.trip import Trip
from app.models.expense import Expense
from app.models.itinerary import ItineraryStop, ItineraryItem
from app.models.activity import Activity


def calculate_trip_budget(trip_id: int) -> Dict[str, Any]:
    """
    Calculates total dynamic trip expenses, category breakdowns,
    daily average costs, and budget health status.
    """
    trip = Trip.query.get(trip_id)
    if not trip:
        return {
            'total_budget': 0.0,
            'total_expenses': 0.0,
            'remaining_budget': 0.0,
            'is_over_budget': False,
            'categories': {},
            'daily_average': 0.0
        }

    # Retrieve all logged expenses for the trip
    expenses = Expense.query.filter_by(trip_id=trip_id).all()

    # Calculate activity costs from itinerary items
    activity_expenses_total = db.session.query(func.sum(Activity.estimated_cost))\
        .join(ItineraryItem, ItineraryItem.activity_id == Activity.id)\
        .join(ItineraryStop, ItineraryItem.stop_id == ItineraryStop.id)\
        .filter(ItineraryStop.trip_id == trip_id)\
        .scalar() or 0.0

    # Categorize explicitly logged expenses
    categories = {
        'Transport': 0.0,
        'Accommodation': 0.0,
        'Activities': float(activity_expenses_total),
        'Meals': 0.0,
        'General': 0.0
    }

    logged_total = 0.0
    for expense in expenses:
        category = expense.category if expense.category in categories else 'General'
        categories[category] += float(expense.amount)
        logged_total += float(expense.amount)

    total_spent = logged_total + float(activity_expenses_total)
    trip_budget = float(trip.budget) if trip.budget else 0.0
    remaining_budget = trip_budget - total_spent
    is_over_budget = total_spent > trip_budget if trip_budget > 0 else False

    # Calculate trip duration and daily average expenditure
    num_days = 1
    if trip.start_date and trip.end_date:
        duration = (trip.end_date - trip.start_date).days + 1
        num_days = max(duration, 1)

    daily_average = total_spent / num_days

    return {
        'trip_id': trip_id,
        'total_budget': round(trip_budget, 2),
        'total_expenses': round(total_spent, 2),
        'remaining_budget': round(remaining_budget, 2),
        'is_over_budget': is_over_budget,
        'categories': {k: round(v, 2) for k, v in categories.items()},
        'daily_average': round(daily_average, 2),
        'num_days': num_days
    }


def get_budget_alerts(trip_id: int) -> List[str]:
    """Generates warning messages if trip expenditure exceeds budget thresholds."""
    summary = calculate_trip_budget(trip_id)
    alerts = []

    if summary['total_budget'] > 0:
        if summary['is_over_budget']:
            over_amount = round(summary['total_expenses'] - summary['total_budget'], 2)
            alerts.append(f"Warning: Trip is over budget by ${over_amount}!")
        elif summary['remaining_budget'] < (summary['total_budget'] * 0.1):
            alerts.append("Alert: You have spent over 90% of your allocated budget.")

    return alerts