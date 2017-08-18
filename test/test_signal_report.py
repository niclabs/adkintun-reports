from datetime import datetime, timedelta
from app import application, db
from test import base_test
from app.report.signal_report_generation import signal_strength_mean_for_antenna

from app.models_server.carrier import Carrier
from app.models_server.sim import Sim
from app.models_server.antenna import Antenna
from app.models_server.gsm_event import GsmEvent


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
        antenna2 = Antenna(cid=2, lac=2, carrier_id=1001)
        antenna2.id = 1000

        event1 = GsmEvent(signal_strength_size=2, signal_strength_mean=10, date=datetime.now())
        sim1.events.append(event1)
        antenna1.gsm_events.append(event1)

        event2 = GsmEvent(signal_strength_size=5, signal_strength_mean=100, date=datetime.now())
        sim2.events.append(event2)
        antenna2.gsm_events.append(event2)

        # should not show in report
        event3 = GsmEvent(signal_strength_size=4, signal_strength_mean=50, date=datetime.now() + timedelta(days=1))
        sim2.events.append(event3)
        antenna1.gsm_events.append(event3)

        event4 = GsmEvent(signal_strength_size=6, signal_strength_mean=150, date=datetime.now())
        sim1.events.append(event4)
        antenna2.gsm_events.append(event4)

        event5 = GsmEvent(signal_strength_size=6, signal_strength_mean=40, date=datetime.now())
        sim1.events.append(event5)
        antenna1.gsm_events.append(event5)

        db.session.add(carrier1)
        db.session.add(carrier2)
        db.session.commit()

    def test_report_generation(self):
        with application.app_context():
            self.populate()
            report = signal_strength_mean_for_antenna()
            self.assertEqual(len(report), 3)

            # carrier 2, antenna 2
            self.assertEqual(report[0]['carrier_id'], 1001)
            self.assertEqual(report[0]['antenna_id'], 1000)
            self.assertEqual(report[0]['observations'], 5)
            self.assertEqual(report[0]['signal_mean'], 100)

            # carrier 1, antenna 2
            self.assertEqual(report[1]['carrier_id'], 1000)
            self.assertEqual(report[1]['antenna_id'], 1000)
            self.assertEqual(report[1]['observations'], 6)
            self.assertEqual(report[1]['signal_mean'], 150)

            # carrier 1, antenna 1
            self.assertEqual(report[2]['carrier_id'], 1000)
            self.assertEqual(report[2]['antenna_id'], 1337)
            self.assertEqual(report[2]['observations'], 8)
            self.assertAlmostEqual(report[2]['signal_mean'], 38.75206, places=5)
