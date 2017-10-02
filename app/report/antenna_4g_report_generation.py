from app import db1
from datetime import datetime
from sqlalchemy import text


# 4g network report
def network_report_for_4g(min_date=datetime(2015, 1, 1), max_date=None):
    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    stmt = text("""
    SELECT
        CASE WHEN gsm_events_4g_capable.network_type = 14 THEN '4G'
        ELSE 'OTHER' END as network_type,
        antennas_4g_capable.id as antenna,
        sims.carrier_id as carrier,
        sum(gsm_events_4g_capable.size) as size
    FROM
        (SELECT DISTINCT gsm_events.antenna_id as id
            FROM gsm_events
            WHERE
                gsm_events.date BETWEEN :min_date AND :max_date AND
                gsm_events.network_type = 14) as antennas_4g_capable,
        (SELECT gsm_events.id, gsm_events.sim_serial_number, gsm_events.date,
                gsm_events.antenna_id, gsm_events.network_type,
                gsm_events.signal_strength_size as size
            FROM
             gsm_events,
             (SELECT DISTINCT gsm_events.device_id
                FROM gsm_events
                WHERE
                    gsm_events.date BETWEEN :min_date AND :max_date AND
                    gsm_events.network_type = 14) as devices_4g_capable
            WHERE
                gsm_events.date BETWEEN :min_date AND :max_date AND
                gsm_events.device_id = devices_4g_capable.device_id
        ) as gsm_events_4g_capable,
        public.sims
    WHERE
        gsm_events_4g_capable.date BETWEEN :min_date AND :max_date AND
        gsm_events_4g_capable.antenna_id = antennas_4g_capable.id AND
        gsm_events_4g_capable.sim_serial_number = sims.serial_number
    GROUP BY
        gsm_events_4g_capable.network_type,
        antennas_4g_capable.id,
        sims.carrier_id""")

    result = db1.session.query().add_columns("network_type", "antenna", "carrier", "size").from_statement(stmt).params(
        min_date=min_date, max_date=max_date)

    final = {}
    for row in result.all():
        network_type = row[0]
        antenna_id = str(row[1])
        carrier = str(row[2])
        size = row[3]
        if carrier not in final:
            final[carrier] = {}
        if antenna_id not in final[carrier]:
            final[carrier][antenna_id] = {'4g_events': 0, 'non_4g_events': 0}
        if network_type == '4G':
            final[carrier][antenna_id]['4g_events'] = size
        elif network_type == 'OTHER':
            final[carrier][antenna_id]['non_4g_events'] = size

    return final
