from app import db2
from app.models_frontend import base_model
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import JSON


class Ranking(base_model.BaseModel):
    __tablename__ = 'ranking'

    id = db2.Column(db2.Integer, primary_key=True, unique=True)
    year = db2.Column(db2.Integer)
    month = db2.Column(db2.Integer)

    # New columns for the new parameters of the raking
    ranking_number = db2.Column(db2.Integer)
    total_bytes = db2.Column(db2.String(100))
    bytes_per_user = db2.Column(db2.Float)
    total_devices = db2.Column(db2.String(100))
    app_name = db2.Column(db2.String(100))

    carrier_id = db2.Column(db2.Integer, db2.ForeignKey('carriers.id'))
    traffic_type = db2.Column(db2.String(20))
    transfer_type = db2.Column(db2.String(20))

    def __init__(self, year=None, month=None, carrier_id=None, traffic_type=None, transfer_type=None,
                 ranking_number=None, total_bytes=None, bytes_per_user=None, total_devices=None, app_name=None):

        self.year = year
        self.month = month
        self.carrier_id = carrier_id
        self.traffic_type = traffic_type
        self.transfer_type = transfer_type
        self.ranking_number = ranking_number
        self.total_bytes = total_bytes
        self.bytes_per_user = bytes_per_user
        self.total_devices = total_devices
        self.app_name = app_name

    def __repr__(self):
        return '<Ranking year:%r, month:%r, traffic_type:%r, transfer_type:%r, carrier_id:%r >' % (self.year, self.month, self.traffic_type, self.transfer_type, self.carrier_id)
