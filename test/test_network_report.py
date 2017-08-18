from datetime import datetime, timedelta
from app import application, db
from test import base_test
from app.report.network_report_generation import network_report_for_carrier

from app.models_server.sim import Sim
from app.models_server.carrier import Carrier
from app.models_server.gsm_event import GsmEvent
from app.models_server.antenna import Antenna


class TestNetworkReport(base_test.BaseTest):

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

        event1 = GsmEvent(network_type=1, date=datetime.now())
        sim1.events.append(event1)
        antenna1.gsm_events.append(event1)

        event2 = GsmEvent(network_type=1, date=datetime.now())
        sim1.events.append(event2)
        antenna1.gsm_events.append(event2)

        event3 = GsmEvent(network_type=1, date=datetime.now())
        sim2.events.append(event3)
        antenna1.gsm_events.append(event3)

        event4 = GsmEvent(network_type=1, date=datetime.now())
        sim1.events.append(event4)
        antenna2.gsm_events.append(event4)

        event5 = GsmEvent(network_type=6, date=datetime.now())
        sim1.events.append(event5)
        antenna2.gsm_events.append(event5)

        # should not show in report
        event6 = GsmEvent(network_type=6, date=datetime.now()+timedelta(days=1))
        sim2.events.append(event6)
        antenna2.gsm_events.append(event6)

        db.session.add(carrier1)
        db.session.add(carrier2)
        db.session.commit()

    def test_report_generation(self):
        with application.app_context():
            self.populate()
            report = network_report_for_carrier()
            self.assertEqual(len(report), 4)

            # carrier_1, on antenna_2, on wifi
            self.assertEqual(report[0]['carrier_id'], 1000)
            self.assertEqual(report[0]['antenna_id'], 1000)
            self.assertEqual(report[0]['network_type'], 6)
            self.assertEqual(report[0]['size'], 1)

            # carrier_1, on antenna_1, on mobile
            self.assertEqual(report[1]['carrier_id'], 1000)
            self.assertEqual(report[1]['antenna_id'], 1337)
            self.assertEqual(report[1]['network_type'], 1)
            self.assertEqual(report[1]['size'], 2)

            # carrier_2, on antenna_1, on mobile
            self.assertEqual(report[2]['carrier_id'], 1001)
            self.assertEqual(report[2]['antenna_id'], 1337)
            self.assertEqual(report[2]['network_type'], 1)
            self.assertEqual(report[2]['size'], 1)

            # carrier_1, on antenna_2, on mobile
            self.assertEqual(report[3]['carrier_id'], 1000)
            self.assertEqual(report[3]['antenna_id'], 1000)
            self.assertEqual(report[3]['network_type'], 1)
            self.assertEqual(report[3]['size'], 1)
