from app import db1
from app.models_server.event import Event


class TrafficEvent(Event):
    '''
    Traffic events model class
    '''
    __tablename__ = 'traffic_events'

    id = db1.Column(db1.Integer, db1.ForeignKey('events.id'), primary_key=True)
    network_type = db1.Column(db1.Integer)
    rx_bytes = db1.Column(db1.BigInteger)
    tx_bytes = db1.Column(db1.BigInteger)
    rx_packets = db1.Column(db1.BigInteger)
    tx_packets = db1.Column(db1.BigInteger)
    tcp_rx_bytes = db1.Column(db1.BigInteger)
    tcp_tx_bytes = db1.Column(db1.BigInteger)


