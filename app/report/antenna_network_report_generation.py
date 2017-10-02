from app import db1
from datetime import datetime
from sqlalchemy import text
from app.models_server.telephony_observation_event import TelephonyObservationEvent
from app.models_server.antenna import Antenna
from app.models_server.sim import Sim


def network_report_for_carrier(min_date=datetime(2015, 1, 1),
                               max_date=None):
    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    stmt = text("""
    SELECT
        gsm_events.network_type,
        antennas.id,
        gsm_events.carrier_id,
        count(gsm_events.id) as size
    FROM
        public.antennas,
        public.gsm_events
    WHERE
        gsm_events.antenna_id = antennas.id AND
        gsm_events.date BETWEEN :min_date AND :max_date
    GROUP BY
        gsm_events.network_type,
        antennas.id,
        gsm_events.carrier_id;""")

    result = db1.session.query(TelephonyObservationEvent.network_type, Antenna.id,
                              Sim.carrier_id).add_columns("size").from_statement(stmt).params(
        min_date=min_date, max_date=max_date)

    final = [dict(network_type=row[0], antenna_id=row[1], carrier_id=row[2], size=row[3]) for row in
             result.all()]

    return final