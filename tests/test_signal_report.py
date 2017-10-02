from datetime import datetime, timedelta
from app import application, db1, db2
from tests import base_test
from app.report import signal_strength_mean_for_antenna
from app.importation import gsm_signal_import

from app.models_server.carrier import Carrier
from app.models_server.sim import Sim
from app.models_server.antenna import Antenna
from app.models_server.gsm_event import GsmEvent

from app.models_frontend.carrier import Carrier as Carrier2
from app.models_frontend.gsm_signal import GsmSignal


class TestSignalReport(base_test.BaseTest):

    def populate(self):
        carrier1 = Carrier(name="test_carrier_1")
        carrier1.id = 1000
        carrier2 = Carrier(name="test_carrier_2")
        carrier2.id = 1001

        sim1 = Sim(serial_number="123", creation_date=datetime.now())
        carrier1.sims.append(sim1)
        sim2 = Sim(serial_number="456", creation_date=datetime.now())
        carrier2.sims.append(sim2)

        antenna1 = Antenna(cid=1, lac=1, carrier_id=1000)
        antenna1.id = 1337
        antenna1.lat = 1
        antenna1.lon = 1
        antenna2 = Antenna(cid=2, lac=2, carrier_id=1001)
        antenna2.id = 1000
        antenna2.lat = 2
        antenna2.lon = 2

        event1 = GsmEvent(signal_strength_size=2, signal_strength_mean=10, date=datetime.now(),
                          sim_serial_number="123", carrier_id=1000)
        antenna1.gsm_events.append(event1)

        event2 = GsmEvent(signal_strength_size=5, signal_strength_mean=75, date=datetime.now(),
                          sim_serial_number="456", carrier_id=1001)
        antenna2.gsm_events.append(event2)

        # should not show in report
        event3 = GsmEvent(signal_strength_size=4, signal_strength_mean=50, date=datetime.now() + timedelta(days=1),
                          sim_serial_number="456", carrier_id=1001)
        antenna1.gsm_events.append(event3)

        event4 = GsmEvent(signal_strength_size=6, signal_strength_mean=90, date=datetime.now(),
                          sim_serial_number="123", carrier_id=1000)
        antenna2.gsm_events.append(event4)

        event5 = GsmEvent(signal_strength_size=6, signal_strength_mean=40, date=datetime.now(),
                          sim_serial_number="123", carrier_id=1000)
        antenna1.gsm_events.append(event5)

        db1.session.add(carrier1)
        db1.session.add(carrier2)
        db1.session.add(antenna1)
        db1.session.add(antenna2)
        db1.session.commit()

    def test_report_generation(self):
        with application.app_context():
            self.populate()
            report = signal_strength_mean_for_antenna()

        self.assertEqual(len(report), 3)

        # carrier 2, antenna 2
        self.assertEqual(report[0]['carrier_id'], 1001)
        self.assertEqual(report[0]['antenna_id'], 1000)
        self.assertEqual(report[0]['observations'], 5)
        self.assertEqual(report[0]['signal_mean'], 75)

        # carrier 1, antenna 2
        self.assertEqual(report[1]['carrier_id'], 1000)
        self.assertEqual(report[1]['antenna_id'], 1000)
        self.assertEqual(report[1]['observations'], 6)
        self.assertEqual(report[1]['signal_mean'], 90)

        # carrier 1, antenna 1
        self.assertEqual(report[2]['carrier_id'], 1000)
        self.assertEqual(report[2]['antenna_id'], 1337)
        self.assertEqual(report[2]['observations'], 8)
        self.assertAlmostEqual(report[2]['signal_mean'], 38.75206, places=5)

    def test_report_importation(self):
        with application.app_context():
            self.populate()
            report = signal_strength_mean_for_antenna()

            carrier1_frontend = Carrier2(name="test_carrier_1")
            carrier2_frontend = Carrier2(name="test_carrier_2")
            carrier1_frontend.id = 1000
            carrier2_frontend.id = 1001

            db2.session.add(carrier1_frontend)
            db2.session.add(carrier2_frontend)
            db2.session.commit()

            gsm_signal_import(report, 2017, 8)
            result = GsmSignal.query.order_by(GsmSignal.antenna_id, GsmSignal.carrier_id).all()

        self.assertEqual(result[0].antenna_id, 1000)
        self.assertEqual(result[0].carrier_id, 1000)
        self.assertEqual(result[0].signal, 90)
        self.assertEqual(result[0].quantity, 6)

        self.assertEqual(result[1].antenna_id, 1000)
        self.assertEqual(result[1].carrier_id, 1001)
        self.assertEqual(result[1].signal, 75)
        self.assertEqual(result[1].quantity, 5)

        self.assertEqual(result[2].antenna_id, 1337)
        self.assertEqual(result[2].carrier_id, 1000)
        self.assertAlmostEqual(result[2].signal, 38.75206, places=5)
        self.assertEqual(result[2].quantity, 8)
