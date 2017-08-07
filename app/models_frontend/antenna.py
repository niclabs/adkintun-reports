from app import db
from app.models_frontend import base_model
from sqlalchemy import UniqueConstraint


class Antenna(base_model.BaseModel):
    __tablename__ = 'antennas'
    __table_args__ = (UniqueConstraint("cid", "lac", "carrier_id", name="antenna_pk"), {})
    __bind_key__ = 'frontend'
    id = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer)
    lac = db.Column(db.Integer)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    carrier_id = db.Column(db.Integer, db.ForeignKey("carriers.id"))
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    gsm_counts = db.relationship('GsmCount', backref='antenna',
                                 lazy='dynamic')
    gsm_signals= db.relationship('GsmSignal', backref='antenna',
                                 lazy='dynamic')

    def __init__(self, id=None, cid=None, lac=None, lat=None, lon=None, carrier_id=None, city_id=None):
        self.id = id
        self.cid = cid
        self.lac = lac
        self.lat = lat
        self.lon = lon
        self.carrier_id = carrier_id
        self.city_id = city_id

    def __repr__(self):
        return '<Antenna, id: %r,  cid: %r, lac: %r, carriers: %r, city: %r>' % (
            self.id, self.cid, self.lac, self.carrier, self.city)
