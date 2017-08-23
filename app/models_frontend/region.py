from app import db2
from app.models_frontend import base_model


class Region(base_model.BaseModel):
    __tablename__ = 'region'
    id = db2.Column(db2.Integer, primary_key=True, unique=True)
    name = db2.Column(db2.String(50))
    cities = db2.relationship('City', backref='region',
                             lazy='dynamic')
    lat = db2.Column(db2.Float)
    lon = db2.Column(db2.Float)

    def __init__(self, id=None, name=None, lat=None, lon=None):
        self.id = id
        self.name = name
        self.lat = lat
        self.lon = lon

    def __repr__(self):
        return '<Region id: %r,  name: %r>' % (self.id, self.name)
