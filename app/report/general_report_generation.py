from app import db1
from datetime import datetime
from sqlalchemy import text


def general_report(min_date=datetime(2015, 1, 1), max_date=None):
    """
    Calculate the report values and return a dictionary.
    :return: a dictionary with summarized data.
    """
    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    total_devices_of_period = total_devices_registered(min_date, max_date)
    total_devices = total_devices_registered(max_date=max_date)

    total_sims_of_period = total_sims_registered(min_date, max_date)
    total_sims = total_sims_registered(max_date=max_date)

    total_gsm_of_period = total_gsm_events(min_date, max_date)
    total_gsm = total_gsm_events(max_date=max_date)

    total_device_carrier_of_period = total_device_for_carrier(min_date, max_date)
    total_device_carrier = total_device_for_carrier(max_date=max_date)

    total_sims_carrier_of_period = total_sims_for_carrier(min_date, max_date)
    total_sims_carrier = total_sims_for_carrier(max_date=max_date)

    total_gsm_carrier_of_period = total_gsm_events_for_carrier(min_date, max_date)
    total_gsm_carrier = total_gsm_events_for_carrier(max_date=max_date)

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
    from app.models_server.device import Device

    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    return Device.query.filter(Device.events != None, Device.creation_date.between(min_date, max_date)).count()


def total_sims_registered(min_date=datetime(2015, 1, 1),
                          max_date=None):
    from app.models_server.sim import Sim

    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    return Sim.query.filter(Sim.creation_date.between(min_date, max_date)).count()


def total_gsm_events(min_date=datetime(2015, 1, 1),
                     max_date=None):
    from app.models_server.gsm_event import GsmEvent

    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    return GsmEvent.query.filter(GsmEvent.date.between(min_date, max_date)).count()


def total_device_for_carrier(min_date=datetime(2015, 1, 1),
                             max_date=None):
    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    stmt = text("""
    SELECT consulta_1.id, count(id) as devices_count
    FROM
    (SELECT DISTINCT devices.device_id, carriers.id
    FROM devices
    JOIN devices_sims ON devices.device_id = devices_sims.device_id
    JOIN sims ON sims.serial_number = devices_sims.sim_id
    JOIN carriers on sims.carrier_id = carriers.id
    WHERE devices.creation_date BETWEEN :min_date AND :max_date) as consulta_1
    GROUP BY consulta_1.id""")

    result = db1.session.query().add_columns("id", "devices_count").from_statement(stmt).params(
        min_date=min_date, max_date=max_date)

    return result.all()


def total_sims_for_carrier(min_date=datetime(2015, 1, 1),
                           max_date=None):
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


def total_gsm_events_for_carrier(min_date=datetime(2015, 1, 1),
                                 max_date=None):
    from app.models_server.gsm_event import GsmEvent

    if not min_date:
        min_date = datetime(2015, 1, 1)

    if not max_date:
        max_date = datetime.now()

    stmt = text("""
    SELECT sims.carrier_id, count(events.id) AS events_count
    FROM gsm_events
    JOIN sims ON gsm_events.sim_serial_number = sims.serial_number
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
