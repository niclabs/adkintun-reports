from datetime import datetime
from app import application, db
from test import base_test
from app.report.app_report_generation import app_report

from app.models_server.device import Device
from app.models_server.sim import Sim
from app.models_server.carrier import Carrier
from app.models_server.application_traffic_event import ApplicationTrafficEvent
from app.models_server.application import Application


class TestAppReport(base_test.BaseTest):

    def populate(self):
        device1 = Device(device_id="1", creation_date=datetime.now())
        device2 = Device(device_id="2", creation_date=datetime.now())
        device3 = Device(device_id="3", creation_date=datetime.now())

        sim1 = Sim(serial_number="123", creation_date=datetime.now())
        sim2 = Sim(serial_number="456", creation_date=datetime.now())

        sim1.devices.append(device1)
        sim1.devices.append(device2)
        sim2.devices.append(device3)

        carrier1 = Carrier(name="test_carrier_1")
        carrier1.id = 1000
        carrier2 = Carrier(name="test_carrier_2")
        carrier2.id = 1001

        carrier1.sims.append(sim1)
        carrier2.sims.append(sim2)

        app1 = Application("test_name1")
        app1.id = 10
        app2 = Application("test_name2")
        app2.id = 20

        event1 = ApplicationTrafficEvent(date=datetime.now(), network_type=1, rx_bytes=1000, tx_bytes=500)
        event2 = ApplicationTrafficEvent(date=datetime.now(), network_type=1, rx_bytes=2500, tx_bytes=1000)
        event3 = ApplicationTrafficEvent(date=datetime.now(), network_type=6, rx_bytes=10000, tx_bytes=2000)
        event4 = ApplicationTrafficEvent(date=datetime.now(), network_type=1, rx_bytes=2000, tx_bytes=1500)
        event5 = ApplicationTrafficEvent(date=datetime.now(), network_type=1, rx_bytes=1500, tx_bytes=750)

        sim1.events.append(event1)
        sim1.events.append(event2)
        sim1.events.append(event3)
        sim2.events.append(event4)
        sim2.events.append(event5)

        device1.events = [event1]
        device2.events = [event2, event3]
        device3.events = [event4, event5]

        app1.application_traffic_event.append(event1)
        app1.application_traffic_event.append(event2)
        app1.application_traffic_event.append(event3)
        app1.application_traffic_event.append(event4)
        app2.application_traffic_event.append(event5)

        db.session.add(carrier1)
        db.session.add(carrier2)
        db.session.commit()

    def test_report_generation(self):
        with application.app_context():
            self.populate()
            report = app_report()

            # test carrier 1, one app, two devices
            self.assertEqual(report[1000]['MOBILE']['DOWNLOAD'][1]['total_bytes'], '3500')
            self.assertEqual(report[1000]['MOBILE']['UPLOAD'][1]['total_bytes'], '1500')
            self.assertEqual(report[1000]['WIFI']['DOWNLOAD'][1]['total_bytes'], '10000')
            self.assertEqual(report[1000]['WIFI']['UPLOAD'][1]['total_bytes'], '2000')

            self.assertEqual(report[1000]['MOBILE']['DOWNLOAD'][1]['app_name'], 'test_name1')
            self.assertEqual(report[1000]['MOBILE']['UPLOAD'][1]['app_name'], 'test_name1')
            self.assertEqual(report[1000]['WIFI']['DOWNLOAD'][1]['app_name'], 'test_name1')
            self.assertEqual(report[1000]['WIFI']['UPLOAD'][1]['app_name'], 'test_name1')

            self.assertEqual(report[1000]['MOBILE']['DOWNLOAD'][1]['total_devices'], 2)
            self.assertEqual(report[1000]['MOBILE']['UPLOAD'][1]['total_devices'], 2)
            self.assertEqual(report[1000]['WIFI']['DOWNLOAD'][1]['total_devices'], 1)
            self.assertEqual(report[1000]['WIFI']['UPLOAD'][1]['total_devices'], 1)

            # test carrier 2, two apps, one device
            self.assertEqual(report[1001]['MOBILE']['DOWNLOAD'][1]['total_bytes'], '2000')
            self.assertEqual(report[1001]['MOBILE']['UPLOAD'][1]['total_bytes'], '1500')
            self.assertEqual(report[1001]['MOBILE']['DOWNLOAD'][2]['total_bytes'], '1500')
            self.assertEqual(report[1001]['MOBILE']['UPLOAD'][2]['total_bytes'], '750')

            self.assertEqual(report[1001]['MOBILE']['DOWNLOAD'][1]['app_name'], 'test_name1')
            self.assertEqual(report[1001]['MOBILE']['UPLOAD'][1]['app_name'], 'test_name1')
            self.assertEqual(report[1001]['MOBILE']['DOWNLOAD'][2]['app_name'], 'test_name2')
            self.assertEqual(report[1001]['MOBILE']['UPLOAD'][2]['app_name'], 'test_name2')

            self.assertEqual(report[1001]['MOBILE']['DOWNLOAD'][1]['total_devices'], 1)
            self.assertEqual(report[1001]['MOBILE']['UPLOAD'][1]['total_devices'], 1)
            self.assertEqual(report[1001]['MOBILE']['DOWNLOAD'][2]['total_devices'], 1)
            self.assertEqual(report[1001]['MOBILE']['UPLOAD'][2]['total_devices'], 1)
