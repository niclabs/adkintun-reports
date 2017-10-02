from app import db1, reportLogger
from datetime import datetime
from sqlalchemy import text


def general_report(init_date, last_date):
    """
    Calculate the report values and return and print them to a JSON file.
    This will be made the night of the first day of the next month of the report.
    :return: None
    """

    total_devices_of_period = total_devices_registered(init_date, last_date)
    total_devices = total_devices_registered(max_date=last_date)

    total_sims_of_period = total_sims_registered(init_date, last_date)
    total_sims = total_sims_registered(max_date=last_date)

    total_gsm_of_period = total_gsm_events(init_date, last_date)
    total_gsm = total_gsm_events(max_date=last_date)

    total_device_carrier_of_period = total_device_for_carrier(init_date, last_date)
    total_device_carrier = total_device_for_carrier(max_date=last_date)

    total_sims_carrier_of_period = total_sims_for_carrier(init_date, last_date)
    total_sims_carrier = total_sims_for_carrier(max_date=last_date)

    total_gsm_carrier_of_period = total_gsm_events_for_carrier(init_date, last_date)
    total_gsm_carrier = total_gsm_events_for_carrier(max_date=last_date)

    final = {
        "total_devices_of_period": total_devices_of_period,
        "total_devices": total_devices,
        "total_sims_of_period": total_sims_of_period,
        "total_sims": total_sims,
        "total_gsm_of_period": total_gsm_of_period,
        "total_gsm": total_gsm,
        "total_gsm_carrier_of_period": serialize_pairs(total_gsm_carrier_of_period),
        "total_gsm_carrier": serialize_pairs(total_gsm_carrier),
        "total_sims_carrier_of_period": serialize_pairs(total_sims_carrier_of_period),
        "total_sims_carrier": serialize_pairs(total_sims_carrier),
        "total_device_carrier_of_period": serialize_pairs(total_device_carrier_of_period),
        "total_device_carrier": serialize_pairs(total_device_carrier)
    }

    return final


def total_devices_registered(min_date=datetime(2015, 1, 1),
                             max_date=None):
    reportLogger.info("Querying total devices registered")
    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()
    from app.models_server.device import Device
    return Device.query.filter(Device.creation_date.between(min_date, max_date)).count()


# Total sim cards registered
def total_sims_registered(min_date=datetime(2015, 1, 1),
                          max_date=None):
    reportLogger.info("Querying total sims registered")
    from app.models_server.sim import Sim

    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    return Sim.query.filter(Sim.creation_date.between(min_date, max_date)).count()


# Total signal measurements registered (GSM events)
def total_gsm_events(min_date=datetime(2015, 1, 1),
                     max_date=None):
    reportLogger.info("Querying total gsm events")
    from app.models_server.gsm_event import GsmEvent

    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    return GsmEvent.query.filter(GsmEvent.date.between(min_date, max_date)).count()


# Devices by company
def total_device_for_carrier(min_date=datetime(2015, 1, 1),
                             max_date=None):
    reportLogger.info("Querying devices per carrier")
    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    stmt = text("""
    SELECT consulta_1.carrier_id, count(device_id) as devices_count
    FROM
    (SELECT DISTINCT devices.device_id, carriers.id as carrier_id
    FROM devices
    JOIN devices_sims ON devices.device_id = devices_sims.device_id
    JOIN sims ON sims.serial_number = devices_sims.sim_id
    JOIN carriers on sims.carrier_id = carriers.id
    WHERE devices.creation_date BETWEEN :min_date AND :max_date) as consulta_1
    GROUP BY consulta_1.carrier_id""")

    result = db1.session.query().add_columns("carrier_id", "devices_count").from_statement(stmt).params(
        min_date=min_date, max_date=max_date)

    return result.all()


# Sims by company
def total_sims_for_carrier(min_date=datetime(2015, 1, 1),
                           max_date=None):
    reportLogger.info("Querying sims per carrier")
    from app.models_server.sim import Sim

    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    stmt = text("""
    SELECT sims.carrier_id, count(*) AS sims_count
    FROM sims
    WHERE sims.creation_date BETWEEN :min_date AND :max_date
    GROUP BY sims.carrier_id""")

    result = db1.session.query(Sim.carrier_id).add_columns("sims_count").from_statement(stmt).params(
        min_date=min_date, max_date=max_date)

    return result.all()


# GSM events by telco
def total_gsm_events_for_carrier(min_date=datetime(2015, 1, 1),
                                 max_date=None):
    reportLogger.info("Querying gsm events per carrier")
    from app.models_server.gsm_event import GsmEvent

    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    stmt = text("""
    SELECT sims.carrier_id, count(gsm_events.id) AS events_count
    FROM gsm_events join sims on gsm_events.sim_serial_number = sims.serial_number
    WHERE gsm_events.date BETWEEN :min_date AND :max_date
    GROUP BY sims.carrier_id """)

    result = db1.session.query(GsmEvent.carrier_id).add_columns("events_count").from_statement(stmt).params(
        min_date=min_date, max_date=max_date)

    return result.all()


def serialize_pairs(args):
    ans = {}
    for a in args:
        ans[str(a[0])] = a[1]
    return ans
