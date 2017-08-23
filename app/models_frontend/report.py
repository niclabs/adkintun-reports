from app import db2
from app.models_frontend import base_model
from sqlalchemy import PrimaryKeyConstraint


class Report(base_model.BaseModel):
    __tablename__ = 'report'
    year = db2.Column(db2.Integer)
    month = db2.Column(db2.Integer)
    type = db2.Column(db2.String)
    carrier_id = db2.Column(db2.Integer, db2.ForeignKey('carriers.id'))
    quantity = db2.Column(db2.Integer)
    __table_args__ = (PrimaryKeyConstraint("year", "month", "type", "carrier_id", name="report_pk"), {})

    def __init__(self, year=None, month=None, type=None, carrier_id=None, quantity=None):
        self.year = year
        self.month = month
        self.type = type
        self.carrier_id = carrier_id
        self.quantity = quantity

    def __repr__(self):
        return '<Report year: %r,  month: %r>, carrier: %r, type: %r, quantity: %r' % (
        self.year, self.month, self.carrier, self.type, self.quantity)
