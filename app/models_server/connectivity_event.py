from app import db1
from app.models_server.event import Event


class ConnectivityEvent(Event):
    '''
    Clase para los eventos de conectividad
    '''
    __tablename__ = 'connectivity_events'
    __mapper_args__ = {'polymorphic_identity': 'connectivity_event'}

    id = db1.Column(db1.Integer, db1.ForeignKey('events.id'), primary_key=True)
    detailed_state = db1.Column(db1.Integer)
    available = db1.Column(db1.Boolean)
    connected = db1.Column(db1.Boolean)
    roaming = db1.Column(db1.Boolean)
    connection_type = db1.Column(db1.Integer)
    connection_type_other = db1.Column(db1.Integer)

    def __init__(self, date=None, app_version_code=None, sim_serial_number=None, device_id=None, detailed_state=None,
                 available=None, connected=None, roaming=None, connection_type=None, connection_type_other=None):
        self.date = date
        self.app_version_code = app_version_code
        self.sim_serial_number = sim_serial_number
        self.device_id = device_id
        self.detailed_state = detailed_state
        self.available = available
        self.connected = connected
        self.roaming = roaming
        self.connection_type = connection_type
        self.connection_type_other = connection_type_other

    def __repr__(self):
        return '<ConnectivityEvent, id: %r, date: %r>' % (self.id, self.date)
