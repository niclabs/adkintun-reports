from app import application, db
from test import base_test
from app.report.signal_report_generation import signal_strength_mean_for_antenna


class TestSignalReport(base_test.BaseTest):

    def populate(self):
        pass

    def test_report_generation(self):
        with application.app_context():
            self.populate()
            report = signal_strength_mean_for_antenna()
