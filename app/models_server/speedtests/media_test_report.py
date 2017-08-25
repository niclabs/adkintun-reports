from app import db1
from app.models_server.speedtests.active_measurement import ActiveMeasurement


class MediaTestReport(ActiveMeasurement):
    '''
    Media test reports model class
    '''
    __tablename__ = "media_test_reports"

    id = db1.Column(db1.Integer, db1.ForeignKey("active_measurements.id"), primary_key=True)
    video_id = db1.Column(db1.String(50))

    # Relationships
    video_results = db1.relationship("VideoResult", backref="media_test_report", lazy="dynamic")

    def __init__(self, network_interface_id=None, date=None, dispatched=None, video_id=None):
        self.network_interface_id = network_interface_id
        self.date = date
        self.dispatched = dispatched
        self.video_id = video_id

    def __repr__(self):
        return '<MediaTestReport, id: %r, date: %r>' % (self.id, self.date)
