import os
from app import create_app, db
from app.models.user import User
from app.models.trip import Trip
from app.models.city import City
from app.models.activity import Activity
from app.models.itinerary import Itinerary
from app.models.expense import Expense

# Get environment config name (defaults to 'development')
env = os.environ.get("FLASK_ENV", "development")
app = create_app()


@app.shell_context_processor
def make_shell_context():
    """Expose application objects directly to the `flask shell` session."""
    return {
        "db": db,
        "User": User,
        "Trip": Trip,
        "City": City,
        "Activity": Activity,
        "Itinerary": Itinerary,
        "Expense": Expense,
    }


if __name__ == "__main__":
    # Retrieve port and host from env, default to standard development port 5000
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "127.0.0.1")
    debug = os.environ.get("FLASK_DEBUG", "True").lower() in ["true", "1", "t"]

    app.run(host=host, port=port, debug=debug)