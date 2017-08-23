from app import db1, application1
from app.models_server import base_model
from app.models_server.device_sim import devices_sims


class Sim(base_model.BaseModel):
    """
    Sim card model class
    """
    __tablename__ = "sims"

    serial_number = db1.Column(db1.String(50), primary_key=True)
    creation_date = db1.Column(db1.Date())
    carrier_id = db1.Column(db1.Integer, db1.ForeignKey("carriers.id"))
    devices = db1.relationship("Device", secondary=devices_sims, backref=db1.backref("sims", lazy="dynamic"),
                              lazy="dynamic")
    events = db1.relationship("Event", backref="sim", lazy="dynamic")

    def __init__(self, serial_number=None, creation_date=None, carrier_id=None):
        self.serial_number = serial_number
        self.creation_date = creation_date
        self.carrier_id = carrier_id

    def __repr__(self):
        return "<Sim, serial_number: %r, creation_date: %r, carrier: %r, carrier_id: %r>" % \
               (self.serial_number, self.creation_date, self.carrier, self.carrier_id)

    @staticmethod
    def get_sim_or_add_it(args):
        """
        Search a sim and retrieve it if exist, else create a new one and retrieve it.
        If there is not serial_number argument, return None
        """
        from datetime import datetime
        if "serial_number" in args:
            sim = Sim.query.filter(Sim.serial_number == args["serial_number"]).first()

            if not sim:
                sim = Sim(serial_number=args["serial_number"], creation_date=datetime.now())
                db1.session.add(sim)
                try:
                    db1.session.commit()
                except Exception as e:
                    db1.session.rollback()
                    application1.logger.error(
                        "Error adding new sim, serial_number:" + str(sim.serial_number) + "-" + str(e))
            return sim
        else:
            return None

    def add_device(self, device):
        from app.models_server.device import Device

        existent_device = self.devices.filter(Device.device_id == device.device_id).first()
        if not existent_device:
            self.devices.append(device)
