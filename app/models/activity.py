from app import db


class Activity(db.Model):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    type = db.Column(db.String(50), nullable=True)
    cost = db.Column(db.Numeric(10, 2), nullable=True)
    duration_mins = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(256), nullable=True)

    city = db.relationship('City', backref='activities')

    def __repr__(self):
        return f'<Activity {self.name}>'