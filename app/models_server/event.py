from app import db1
from app.models_server.base_model import BaseModel


class Event(BaseModel):
    '''
    Events model class
    '''
    __tablename__ = 'events'

    id = db1.Column(db1.Integer, primary_key=True)
    date = db1.Column(db1.DateTime)
    app_version_code = db1.Column(db1.String(10))
    sim_serial_number = db1.Column(db1.String(50), db1.ForeignKey("sims.serial_number"))
    device_id = db1.Column(db1.String(50), db1.ForeignKey("devices.device_id"))

    # Herencia
    type = db1.Column(db1.String(50))
    __mapper_args__ = {'polymorphic_on': type}
