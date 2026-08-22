from datetime import datetime, timezone
from app import db


class Trip(db.Model):
    __tablename__ = 'trips'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)

    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    budget = db.Column(db.Numeric(10, 2), default=0.0)

    cover_photo_url = db.Column(db.String(256), nullable=True)
    is_public = db.Column(db.Boolean, default=False, nullable=False)
    status = db.Column(db.String(32), default='upcoming', nullable=False)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    owner = db.relationship('User', backref=db.backref('trips', lazy=True))

    @property
    def title(self):
        return self.name

    @title.setter
    def title(self, value):
        self.name = value

    def __init__(self, **kwargs):
        if 'title' in kwargs and 'name' not in kwargs:
            kwargs['name'] = kwargs.pop('title')
        super().__init__(**kwargs)

    def __repr__(self):
        return f'<Trip {self.name}>'