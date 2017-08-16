from app import application, db
from test import base_test
from app.report.network_report_generation import network_report_for_carrier


class TestNetworkReport(base_test.BaseTest):

    def populate(self):
        pass

    def test_report_generation(self):
        with application.app_context():
            self.populate()
            report = network_report_for_carrier()
