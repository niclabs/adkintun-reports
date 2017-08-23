from app import db2
from app.models_frontend import base_model
from sqlalchemy import PrimaryKeyConstraint


class GsmCount(base_model.BaseModel):
    __tablename__ = 'gsm_count'
    year = db2.Column(db2.Integer)
    month = db2.Column(db2.Integer)
    antenna_id = db2.Column(db2.Integer, db2.ForeignKey('antennas.id'))
    carrier_id = db2.Column(db2.Integer, db2.ForeignKey('carriers.id'))
    network_type = db2.Column(db2.Integer, db2.ForeignKey('network_type.id'))
    quantity = db2.Column(db2.Integer)
    __table_args__ = (
        PrimaryKeyConstraint("year", "month", "antenna_id", "network_type", "carrier_id", name="gsm_count_pk"), {})

    def __init__(self, year=None, month=None, antenna_id=None, network_type=None, carrier_id=None, quantity=None):
        self.year = year
        self.month = month
        self.antenna_id = antenna_id
        self.network_type = network_type
        self.carrier_id = carrier_id
        self.quantity = quantity

    def __repr__(self):
        return '<GsmCount year:%r, month:%r, antenna:%r, network_type:%r, carrier:%r >' % (
        self.year, self.month, self.antenna, self.network_type, self.carrier)
