from app import db
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
        telephony_observation_events.network_type,
        antennas.id,
         sims.carrier_id,
        count(gsm_events.id) as size

    FROM
        public.antennas,
        public.gsm_events,
        public.events,
        public.telephony_observation_events,
        public.sims
    WHERE
        gsm_events.antenna_id = antennas.id AND
        gsm_events.id = telephony_observation_events.id AND
        events.id = gsm_events.id AND
        events.sim_serial_number = sims.serial_number AND
        events.date BETWEEN :min_date AND :max_date
    GROUP BY
        telephony_observation_events.network_type,
        antennas.id,
        sims.carrier_id;""")

    result = db.session.query(TelephonyObservationEvent.network_type, Antenna.id,
                              Sim.carrier_id).add_columns("size").from_statement(stmt).params(
        min_date=min_date, max_date=max_date)

    final = [dict(network_type=row[0], antenna_id=row[1], carrier_id=row[2], size=row[3]) for row in
             result.all()]

    return final
