from app import db


class City(db.Model):
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    country = db.Column(db.String(100), nullable=False)
    cost_index = db.Column(db.Integer, nullable=True)
    popularity = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(256), nullable=True)

    def __repr__(self):
        return f'<City {self.name}, {self.country}>'