from app import db2
from app.models_frontend import base_model
from sqlalchemy import PrimaryKeyConstraint


class GsmSignal(base_model.BaseModel):
    __tablename__ = 'gsm_signal'
    year = db2.Column(db2.Integer)
    month = db2.Column(db2.Integer)
    antenna_id = db2.Column(db2.Integer, db2.ForeignKey('antennas.id'))
    carrier_id = db2.Column(db2.Integer, db2.ForeignKey('carriers.id'))
    signal = db2.Column(db2.Float)
    quantity = db2.Column(db2.Integer)
    __table_args__ = (
        PrimaryKeyConstraint("year", "month", "antenna_id", "carrier_id", name="gsm_signal_pk"), {})

    def __init__(self, year=None, month=None, antenna_id=None, carrier_id=None, signal=None, quantity=None):
        self.year = year
        self.month = month
        self.antenna_id = antenna_id
        self.signal = signal
        self.carrier_id = carrier_id
        self.quantity = quantity

    def __repr__(self):
        return '<GsmSignal year:%r, month:%r, antenna:%r, carrier:%r >' % (
        self.year, self.month, self.antenna, self.carrier)
