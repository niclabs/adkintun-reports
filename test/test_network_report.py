from datetime import datetime, timedelta
from app import application, db1, db2
from test import base_test
from app.report import network_report_for_carrier
from app.importation import gsm_count_import

from app.models_server.sim import Sim
from app.models_server.carrier import Carrier
from app.models_server.gsm_event import GsmEvent
from app.models_server.antenna import Antenna

from app.models_frontend.carrier import Carrier as Carrier2
from app.models_frontend.network_type import NetworkType
from app.models_frontend.gsm_count import GsmCount


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
        antenna1.lat = 1
        antenna1.lon = 1
        antenna2 = Antenna(cid=2, lac=2, carrier_id=1001)
        antenna2.id = 1000
        antenna2.lat = 2
        antenna2.lon = 2

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

        db1.session.add(carrier1)
        db1.session.add(carrier2)
        db1.session.commit()

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

    def test_report_importation(self):
        with application.app_context():
            self.populate()
            report = network_report_for_carrier()

            carrier1_frontend = Carrier2(name="test_carrier_1")
            carrier2_frontend = Carrier2(name="test_carrier_2")
            carrier1_frontend.id = 1000
            carrier2_frontend.id = 1001
            network_type1 = NetworkType(net_id=1, name='mobile')
            network_type2 = NetworkType(net_id=6, name='wifi')

            db2.session.add(carrier1_frontend)
            db2.session.add(carrier2_frontend)
            db2.session.add(network_type1)
            db2.session.add(network_type2)
            db2.session.commit()

            gsm_count_import(report, 2017, 8)
            result = GsmCount.query.order_by(GsmCount.antenna_id, GsmCount.carrier_id, GsmCount.network_type).all()

        self.assertEqual(result[0].antenna_id, 1000)
        self.assertEqual(result[0].carrier_id, 1000)
        self.assertEqual(result[0].network_type, 1)
        self.assertEqual(result[0].quantity, 1)

        self.assertEqual(result[1].antenna_id, 1000)
        self.assertEqual(result[1].carrier_id, 1000)
        self.assertEqual(result[1].network_type, 6)
        self.assertEqual(result[1].quantity, 1)

        self.assertEqual(result[2].antenna_id, 1337)
        self.assertEqual(result[2].carrier_id, 1000)
        self.assertEqual(result[2].network_type, 1)
        self.assertEqual(result[2].quantity, 2)

        self.assertEqual(result[3].antenna_id, 1337)
        self.assertEqual(result[3].carrier_id, 1001)
        self.assertEqual(result[3].network_type, 1)
        self.assertEqual(result[3].quantity, 1)
