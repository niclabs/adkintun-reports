from app import db1, application1
from app.models_server.base_model import BaseModel


class NetworkInterface(BaseModel):
    '''
    network interface model class
    '''
    __tablename__ = 'network_interfaces'

    id = db1.Column(db1.Integer, primary_key=True)
    active_interface = db1.Column(db1.Integer)
    ssid = db1.Column(db1.String(50))
    bssid = db1.Column(db1.String(50))
    gsm_cid = db1.Column(db1.Integer)
    gsm_lac = db1.Column(db1.Integer)
    network_type = db1.Column(db1.Integer)

    def __init__(self, active_interface=None, ssid=None, bssid=None, gsm_cid=None, gsm_lac=None, network_type=None):
        self.active_interface = active_interface
        self.ssid = ssid
        self.bssid = bssid
        self.gsm_cid = gsm_cid
        self.gsm_lac = gsm_lac
        self.network_type = network_type

    def __repr__(self):
        return '<NetworkInterface, id: %r, Active interface: %r>' % (self.id, self.active_interface)

    @staticmethod
    def add_network_interface(args: dict):
        """
        Create a new network interface object from a dict
        :param args: dict with network interface data
        :return: Network interface object
        """
        if "active_interface" in args and "network_type" in args:
            if "ssid" in args and "bssid" in args and "gsm_cid" in args and "gsm_lac" in args:
                ni = NetworkInterface(active_interface=args["active_interface"], ssid=args["ssid"], bssid=args["bssid"],
                                      gsm_cid=args["gsm_cid"], gsm_lac=args["gsm_lac"],
                                      network_type=args["network_type"])
                db1.session.add(ni)
            if "ssid" in args and "bssid" in args:
                ni = NetworkInterface(active_interface=args["active_interface"], ssid=args["ssid"], bssid=args["bssid"],
                                      network_type=args["network_type"])
                db1.session.add(ni)
            elif "gsm_cid" in args and "gsm_lac" in args:
                ni = NetworkInterface(active_interface=args["active_interface"], gsm_cid=args["gsm_cid"], gsm_lac=args["gsm_lac"],
                                      network_type=args["network_type"])
                db1.session.add(ni)

            try:
                db1.session.commit()
            except Exception as e:
                db1.session.rollback()
                application1.logger.error("Error adding network interface, network type:" + args["network_type"])
                return None
            return ni
        else:
            return None
