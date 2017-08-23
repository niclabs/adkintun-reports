from app import db2
from app.models_frontend import base_model


class City(base_model.BaseModel):
    __tablename__ = 'city'
    id = db2.Column(db2.Integer, primary_key=True, unique=True)
    name = db2.Column(db2.String(50))
    antennas = db2.relationship('Antenna', backref='city',
                               lazy='dynamic')
    region_id = db2.Column(db2.Integer, db2.ForeignKey('region.id'))
    lat = db2.Column(db2.Float)
    lon = db2.Column(db2.Float)


    def __init__(self, id, name=None, region_id=None):
        self.id = id
        self.name = name
        self.region_id = region_id

    def __repr__(self):
        return '<City name: %r, region: %r, lat: %r, lon: %r>' % (self.name, self.region, self.lat, self.lon)
