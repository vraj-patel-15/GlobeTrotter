from datetime import datetime, timezone
from app import db

class Trip(db.Model):
    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    
    cover_photo_url = db.Column(db.String(256), nullable=True)
    is_public = db.Column(db.Boolean, default=False, nullable=False)
    status = db.Column(db.String(32), default='upcoming', nullable=False)
    
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    owner = db.relationship('User', backref=db.backref('trips', lazy=True))

    def __repr__(self):
        return f'<Trip {self.name}>'