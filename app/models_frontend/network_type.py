from app import db2
from app.models_frontend import base_model


class NetworkType(base_model.BaseModel):
    __tablename__ = 'network_type'
    id = db2.Column(db2.Integer, primary_key=True, unique=True)
    name = db2.Column(db2.String(10))
    type = db2.Column(db2.String(5))

    def __init__(self, net_id=None, name=None, net_type=None):
        self.id = net_id
        self.name = name
        self.type = net_type

    def __repr__(self):
        return '<Network type id: %r, name: %r, type: %r>' % (self.id, self.name, self.type)
