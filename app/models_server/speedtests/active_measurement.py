from app import db1
from app.models_server import base_model


class ActiveMeasurement(base_model.BaseModel):
    """
    Active measurement model class
    """
    __tablename__ = "active_measurements"
    id = db1.Column(db1.Integer, primary_key=True)
    # ver como guardar en su momento
    network_interface_id = db1.Column(db1.Integer, db1.ForeignKey("network_interfaces.id"))
    # transformar al guardar
    date = db1.Column(db1.DateTime)
    dispatched = db1.Column(db1.Boolean)
    sim_serial_number = db1.Column(db1.String(50), db1.ForeignKey("sims.serial_number"))
    device_id = db1.Column(db1.String(50), db1.ForeignKey("devices.device_id"))
    app_version_code = db1.Column(db1.String(10))

    # Herencia
    type = db1.Column(db1.String(50))
    __mapper_args__ = {'polymorphic_on': type}
