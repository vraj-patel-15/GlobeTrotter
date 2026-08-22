from app import db
from app.models.trip import Trip

class Stop(db.Model):
    __tablename__ = 'stops'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    order_index = db.Column(db.Integer, default=0)
    budget = db.Column(db.Numeric(10, 2), default=0)

    @property
    def arrival_date(self):
        return self.start_date

    @arrival_date.setter
    def arrival_date(self, value):
        self.start_date = value

    @property
    def departure_date(self):
        return self.end_date

    @departure_date.setter
    def departure_date(self, value):
        self.end_date = value

    trip = db.relationship('Trip', backref=db.backref('stops', cascade='all, delete-orphan'))
    city = db.relationship('City')


class TripActivity(db.Model):
    __tablename__ = 'trip_activities'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    stop_id = db.Column(db.Integer, db.ForeignKey('stops.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)
    day_number = db.Column(db.Integer, default=1)
    notes = db.Column(db.Text, nullable=True)

    stop = db.relationship('Stop', backref=db.backref('activities', cascade='all, delete-orphan'))
    activity = db.relationship('Activity')


ItineraryStop = Stop
ItineraryItem = TripActivity