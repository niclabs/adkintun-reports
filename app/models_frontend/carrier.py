from app import db2
from app.models_frontend import base_model


class Carrier(base_model.BaseModel):
    __tablename__ = 'carriers'
    id = db2.Column(db2.Integer, primary_key=True, unique=True)
    name = db2.Column(db2.String(50))
    mcc = db2.Column(db2.Integer)
    mnc = db2.Column(db2.Integer)
    reports = db2.relationship('Report', backref='carrier',
                              lazy='dynamic')
    rankings = db2.relationship('Ranking', backref='carrier',
                               lazy='dynamic')
    antennas = db2.relationship("Antenna", backref='carrier', lazy='dynamic')

    gsm_counts = db2.relationship('GsmCount', backref='carrier',
                                 lazy='dynamic')
    gsm_signals = db2.relationship('GsmSignal', backref='carrier',
                                  lazy='dynamic')

    def __init__(self, name=None, mcc=None, mnc=None):
        self.name = name
        self.mcc = mcc
        self.mnc = mnc

    def __repr__(self):
        return '<Carrier %r>' % (self.name)
