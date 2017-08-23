from sqlalchemy import UniqueConstraint

from app import db1, application1
from app.models_server import base_model


class Antenna(base_model.BaseModel):
    """
    Antenna Class.
    """
    __tablename__ = "antennas"
    __table_args__ = (UniqueConstraint("cid", "lac", "carrier_id", name="antenna_pk"), {})
    id = db1.Column(db1.Integer, primary_key=True)
    cid = db1.Column(db1.Integer)
    lac = db1.Column(db1.Integer)
    lat = db1.Column(db1.Float)
    lon = db1.Column(db1.Float)
    carrier_id = db1.Column(db1.Integer, db1.ForeignKey("carriers.id"))
    gsm_events = db1.relationship("GsmEvent", backref="antenna",
                                 lazy="dynamic")

    def __init__(self, cid=None, lac=None, lat=None, lon=None, carrier_id=None):
        self.cid = cid
        self.lac = lac
        self.lat = lat
        self.lon = lon
        self.carrier_id = carrier_id

    def __repr__(self):
        return "<Antenna, id: %r,  cid: %r, lac: %r, carrier: %r,>" % (self.id, self.cid, self.lac, self.carrier_id)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            "id": self.id,
            "cid": self.cid,
            "lac": self.lac,
            "lat": self.lat,
            "lon": self.lon,
            "carrier_id": self.carrier_id
        }

    @staticmethod
    def get_antenna_or_add_it(lac, cid, mnc, mcc):
        """
        Search an antenna and retrieve it if exist, else create a new one and retrieve it.
        """
        if mnc and mcc and lac and cid:
            from app.models.carrier import Carrier
            carrier = Carrier.query.filter(Carrier.mnc == mnc, Carrier.mcc == mcc).first()
            antenna = Antenna.query.filter(Antenna.lac == lac, Antenna.cid == cid,
                                           Antenna.carrier_id == carrier.id).first()
            if not antenna:
                antenna = Antenna(lac=lac, cid=cid, carrier_id=carrier.id)
                db1.session.add(antenna)
                try:
                    db1.session.commit()
                    application1.logger.info(
                        "New antenna added: lac:" + str(lac) + ", cid:" + str(cid) + ", carrier_id:" + str(carrier.id))
                except Exception as e:
                    db1.session.rollback()
                    application1.logger.error("Error adding antenna to database: lac:" + str(lac) + ", cid:" + str(
                        cid) + ", carrier_id:" + str(carrier.id) + "-" + str(e))
            return antenna
        else:
            return None
