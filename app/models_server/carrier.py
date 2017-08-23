from typing import TypeVar

from app import db1, application1
from app.models_server import base_model

class Carrier(base_model.BaseModel):
    '''
    Carrier model class
    '''

    __tablename__ = 'carriers'
    id = db1.Column(db1.Integer, primary_key=True, unique=True)
    name = db1.Column(db1.String(50))
    mcc = db1.Column(db1.Integer)
    mnc = db1.Column(db1.Integer)
    sims = db1.relationship('Sim', backref='carrier', lazy='dynamic')
    telephony_observation_events = db1.relationship('TelephonyObservationEvent', backref='carrier', lazy='dynamic')
    antennas = db1.relationship("Antenna", backref='carrier', lazy='dynamic')

    # for Type hints
    C = TypeVar("Carrier")

    def __init__(self, name=None, mcc=None, mnc=None):
        self.name = name
        self.mcc = mcc
        self.mnc = mnc

    def __repr__(self):
        return '<Carrier %r>' % (self.name)

    def add_sim(self, sim):
        """
        Add sim to sims parameter in a carrier, just if it was not previously added.
        """
        from app.models_server.sim import Sim
        existent_sim = self.sims.filter(Sim.serial_number == sim.serial_number).first()
        if not existent_sim:
            self.sims.append(sim)

    @staticmethod
    def add_new_carrier(mnc: int, mcc: int, name="Unknown") -> None:
        """
        Add new carrier, giving just the mnc and mcc
        :param mnc: value of mnc code
        :param mcc: value of mcc code
        :param name: name of the carrier
        :return: None
        """
        carrier = Carrier(mnc=mnc, mcc=mcc, name=name)
        carrier.id = int(str(mcc) + str(mnc))
        db1.session.add(carrier)
        try:
            db1.session.commit()
        except Exception as e:
            db1.session.rollback()
            application1.logger.error(
                "Error adding new carrier, mnc:" + str(mnc) + ", mcc: " + str(mcc) + " - " + str(e))

    @staticmethod
    def get_carrier_or_add_it(mnc: int, mcc: int) -> C:
        """
        Search a carrier and retrieve it if exist, else create a new one and retrieve it.
        :param mnc: value of mnc code
        :param mcc: value of mcc code
        :return: Carrier
        """
        if mnc and mcc:
            carrier = Carrier.query.filter(Carrier.mnc == mnc, Carrier.mcc == mcc).first()
            if not carrier:
                Carrier.add_new_carrier(mnc, mcc)
                application1.logger.info("New carrier added: mnc:" + str(mnc) + ", mcc: " + str(mcc))
                carrier = Carrier.query.filter(Carrier.mnc == mnc, Carrier.mcc == mcc).first()
            return carrier
        else:
            return None
