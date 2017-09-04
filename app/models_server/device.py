from app import db1, application
from app.models_server import base_model


class Device(base_model.BaseModel):
    """
    Device model class
    """
    __tablename__ = "devices"
    device_id = db1.Column(db1.String(50), primary_key=True)
    brand = db1.Column(db1.String(50))
    board = db1.Column(db1.String(50))
    build_id = db1.Column(db1.String(100))
    creation_date = db1.Column(db1.Date())
    device = db1.Column(db1.String(50))
    hardware = db1.Column(db1.String(50))
    manufacturer = db1.Column(db1.String(50))
    model = db1.Column(db1.String(50))
    release = db1.Column(db1.String(50))
    release_type = db1.Column(db1.String(50))
    product = db1.Column(db1.String(50))
    sdk = db1.Column(db1.Integer)
    events = db1.relationship("Event", backref="device", lazy="dynamic")

    def __init__(self, device_id, brand=None, board=None, build_id=None, device=None, hardware=None,
                 manufacturer=None, model=None, release=None, release_type=None, product=None, sdk=None,
                 creation_date=None):
        self.device_id = device_id
        self.brand = brand
        self.board = board
        self.build_id = build_id
        self.device = device
        self.hardware = hardware
        self.manufacturer = manufacturer
        self.model = model
        self.release = release
        self.release_type = release_type
        self.product = product
        self.sdk = sdk
        self.creation_date = creation_date

    def __repr__(self):
        return "<Device %r, device_id %r>" % (self.device, self.device_id)

    @staticmethod
    def get_device_or_add_it(args):
        """
        Search a device and retrieve it if exist, else create a new one and retrieve it adding it in a new session.
        """
        from datetime import datetime
        if "device_id" in args:
            device = Device.query.filter(Device.device_id == args["device_id"]).first()
            if not device:
                device = Device(
                    device_id=args["device_id"],
                    brand=args["brand"],
                    board=args["board"],
                    build_id=args["build_id"],
                    device=args["device"],
                    hardware=args["hardware"],
                    manufacturer=args["manufacturer"],
                    model=args["model"],
                    release=args["release"],
                    release_type=args["release_type"],
                    product=args["product"],
                    sdk=args["sdk"],
                    creation_date=datetime.now())
                db1.session.add(device)
                try:
                    db1.session.commit()
                except Exception as e:
                    db1.session.rollback()
                    application.logger.error("Error adding device to database - " + str(e))
            return device
        else:
            return None
