from app import db1
from app.models_server.event import Event
from sqlalchemy.ext.declarative import declared_attr


class TelephonyObservationEvent(Event):
    '''
    Telephony observation model class
    '''
    __tablename__ = 'telephony_observation_events'

    id = db1.Column(db1.Integer, db1.ForeignKey('events.id'), primary_key=True)

    telephony_standard = db1.Column(db1.Integer)
    network_type = db1.Column(db1.Integer)
    signal_strength_size = db1.Column(db1.Integer)
    signal_strength_mean = db1.Column(db1.Float)
    signal_strength_variance = db1.Column(db1.Float)
    mnc = db1.Column(db1.Integer)
    mcc = db1.Column(db1.Integer)

    @declared_attr
    def carrier_id(cls):
        return db1.Column(db1.Integer, db1.ForeignKey("carriers.id"))

