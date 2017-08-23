from app import db1
from app.models_server.telephony_observation_event import TelephonyObservationEvent


class GsmEvent(TelephonyObservationEvent):
    '''
    Gsm observation events model class
    '''
    __tablename__ = 'gsm_events'
    __mapper_args__ = {'polymorphic_identity': 'gsm_event'}

    id = db1.Column(db1.Integer, db1.ForeignKey('telephony_observation_events.id'), primary_key=True)
    gsm_psc = db1.Column(db1.Integer)
    signal_ber_size = db1.Column(db1.Integer)
    signal_ber_mean = db1.Column(db1.Float)
    signal_ber_variance = db1.Column(db1.Float)
    gsm_lac = db1.Column(db1.Integer)
    gsm_cid = db1.Column(db1.Integer)
    antenna_id = db1.Column(db1.Integer, db1.ForeignKey('antennas.id'))

    def __init__(self, date=None, app_version_code=None, sim_serial_number=None, device_id=None,
                 telephony_standard=None, network_type=None, gsm_psc=None, gsm_cid=None, gsm_lac=None,
                 signal_strength_size=None, signal_strength_mean=None, signal_strength_variance=None,
                 signal_ber_size=None, signal_ber_mean=None, signal_ber_variance=None, mnc=None, mcc=None):
        self.date = date
        self.app_version_code = app_version_code
        self.sim_serial_number = sim_serial_number
        self.device_id = device_id
        self.telephony_standard = telephony_standard
        self.network_type = network_type
        self.signal_strength_size = signal_strength_size
        self.signal_strength_mean = signal_strength_mean
        self.signal_strength_variance = signal_strength_variance
        self.gsm_psc = gsm_psc
        self.signal_ber_size = signal_ber_size
        self.signal_ber_mean = signal_ber_mean
        self.signal_ber_variance = signal_ber_variance
        self.gsm_cid = gsm_cid
        self.gsm_lac = gsm_lac
        self.mnc = mnc
        self.mcc = mcc

    def __repr__(self):
        return '<GsmEvent, id: %r, date: %r>' % (self.id, self.date)
