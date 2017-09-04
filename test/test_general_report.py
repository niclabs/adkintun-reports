from datetime import datetime, timedelta
from app import application, db1, db2
from test import base_test
from app.report import general_report
from app.importation import report_import

from app.models_server.device import Device
from app.models_server.sim import Sim
from app.models_server.carrier import Carrier
from app.models_server.gsm_event import GsmEvent

from app.models_frontend.carrier import Carrier as Carrier2
from app.models_frontend.report import Report


class TestGeneralReport(base_test.BaseTest):

    def populate(self):
        device1 = Device(device_id="1", creation_date=datetime.now() + timedelta(days=-2))
        device2 = Device(device_id="2", creation_date=datetime.now())
        device3 = Device(device_id="3", creation_date=datetime.now())
        device4 = Device(device_id="4", creation_date=datetime.now())

        sim1 = Sim(serial_number="123", creation_date=datetime.now() + timedelta(days=-2))
        sim2 = Sim(serial_number="456", creation_date=datetime.now())
        sim3 = Sim(serial_number="789", creation_date=datetime.now())

        sim1.devices.append(device1)
        sim1.devices.append(device2)
        sim2.devices.append(device1)
        sim2.devices.append(device3)
        sim3.devices.append(device4)

        carrier1 = Carrier(name="test_carrier_1")
        carrier2 = Carrier(name="test_carrier_2")
        carrier1.id = 1000
        carrier2.id = 1002

        carrier1.sims.append(sim1)
        carrier1.sims.append(sim2)
        carrier2.sims.append(sim3)

        event1 = GsmEvent(date=datetime.now() + timedelta(days=-2))
        event2 = GsmEvent(date=datetime.now())
        event3 = GsmEvent(date=datetime.now())
        event4 = GsmEvent(date=datetime.now())
        event5 = GsmEvent(date=datetime.now())

        sim1.events.append(event1)
        sim1.events.append(event2)
        sim2.events.append(event3)
        sim2.events.append(event4)
        sim3.events.append(event5)

        device1.events = [event2, event3]
        device2.events = [event1]
        device3.events = [event4]
        device4.events = [event5]

        db1.session.add(carrier1)
        db1.session.add(carrier2)
        db1.session.commit()

    def test_report_generation(self):
        with application.app_context():

            self.populate()
            report = general_report(datetime.now() + timedelta(days=-1), None)

        # tests for total data
        self.assertEqual(report['total_devices'], 4)
        self.assertEqual(report['total_sims'], 3)
        self.assertEqual(report['total_gsm'], 5)

        self.assertEqual(report['total_device_carrier']['1000'], 3)
        self.assertEqual(report['total_device_carrier']['1002'], 1)
        self.assertEqual(report['total_sims_carrier']['1000'], 2)
        self.assertEqual(report['total_sims_carrier']['1002'], 1)
        self.assertEqual(report['total_gsm_carrier']['1000'], 4)
        self.assertEqual(report['total_gsm_carrier']['1002'], 1)

        # tests for filtered data
        self.assertEqual(report['total_devices_of_period'], 3)
        self.assertEqual(report['total_sims_of_period'], 2)
        self.assertEqual(report['total_gsm_of_period'], 4)

        self.assertEqual(report['total_device_carrier_of_period']['1000'], 2)
        self.assertEqual(report['total_device_carrier_of_period']['1002'], 1)
        self.assertEqual(report['total_sims_carrier_of_period']['1000'], 1)
        self.assertEqual(report['total_sims_carrier_of_period']['1002'], 1)
        self.assertEqual(report['total_gsm_carrier_of_period']['1000'], 3)
        self.assertEqual(report['total_gsm_carrier_of_period']['1002'], 1)

    def test_report_importation(self):
        with application.app_context():

            self.populate()
            report = general_report(datetime.now() + timedelta(days=-1), None)

            carrier1_frontend = Carrier2(name="test_carrier_1")
            carrier2_frontend = Carrier2(name="test_carrier_2")
            carrier1_frontend.id = 1000
            carrier2_frontend.id = 1002

            db2.session.add(carrier1_frontend)
            db2.session.add(carrier2_frontend)
            db2.session.commit()

            report_import(report, 2017, 8)

            results = Report.query.order_by(Report.type, Report.carrier_id).all()

        self.assertEqual(results[0].type, 'total_device_carrier')
        self.assertEqual(results[0].carrier_id, 1000)
        self.assertEqual(results[0].quantity, 3)

        self.assertEqual(results[1].type, 'total_device_carrier')
        self.assertEqual(results[1].carrier_id, 1002)
        self.assertEqual(results[1].quantity, 1)

        self.assertEqual(results[2].type, 'total_device_carrier_of_period')
        self.assertEqual(results[2].carrier_id, 1000)
        self.assertEqual(results[2].quantity, 2)

        self.assertEqual(results[4].type, 'total_gsm_carrier')
        self.assertEqual(results[4].carrier_id, 1000)
        self.assertEqual(results[4].quantity, 4)

        self.assertEqual(results[6].type, 'total_gsm_carrier_of_period')
        self.assertEqual(results[6].carrier_id, 1000)
        self.assertEqual(results[6].quantity, 3)

        self.assertEqual(results[8].type, 'total_sims_carrier')
        self.assertEqual(results[8].carrier_id, 1000)
        self.assertEqual(results[8].quantity, 2)

        self.assertEqual(results[10].type, 'total_sims_carrier_of_period')
        self.assertEqual(results[10].carrier_id, 1000)
        self.assertEqual(results[10].quantity, 1)
