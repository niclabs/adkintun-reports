import json
from app import application1, application2, db2
from app.models_server.antenna import Antenna as Antenna1
from app.models_frontend.antenna import Antenna as Antenna2
from app.models_frontend.carrier import Carrier
from app.models_frontend.report import Report
from app.models_frontend.ranking import Ranking
from app.models_frontend.gsm_signal import GsmSignal
from app.models_frontend.gsm_count import GsmCount
from sqlalchemy.exc import IntegrityError


# Handles the general report importation (Named general_report_month_year)
def report_import(data, year, month):
    carriers = Carrier.query.all()
    carrierIds = [c.id for c in carriers]

    try:
        for report_type, element in data.items():

            if type(element) == dict:

                for carrier, quantity in element.items():
                    if carrier.isdigit():
                        carrier_id = int(carrier)
                    else:
                        continue
                        # Ignoring the carriers not listed
                    if carrier_id not in carrierIds:
                        continue
                    insert_or_update_report(Report(year, month, report_type, carrier_id, quantity))
            else:
                carrier_id = 0
                insert_or_update_report(Report(year, month, report_type, carrier_id, element))
    except IntegrityError:
        db2.session.rollback()


def insert_or_update_report(report):
    try:
        db2.session.add(report)
        db2.session.commit()
    except IntegrityError:
        db2.session.rollback()
        db_report = Report.query.filter_by(year=report.year, month=report.month,
                                           carrier_id=report.carrier_id, type=report.type).first()
        if db_report is not None:
            db_report.quantity = report.quantity
            db2.session.commit()


# Handles the ranking import reports
def ranking_import(data, year, month):
    carriers = Carrier.query.all()
    carrierIds = [c.id for c in carriers]

    try:
        for carrier, dict in data.items():

            if carrier == 'ALL_CARRIERS':
                carrier_id = 0
            else:
                carrier_id = int(carrier)

            if carrier_id not in carrierIds:
                continue

            for traffic_type, dict in dict.items():

                for transfer_type, rank in dict.items():

                    for ranking_number in sorted(rank.keys()):

                        ranking_info = rank[ranking_number]

                        insert_or_update_ranking(Ranking(year=year, month=month, carrier_id=carrier_id,
                                                         traffic_type=traffic_type.lower(),
                                                         transfer_type=transfer_type.lower(),
                                                         ranking_number=int(ranking_number),
                                                         app_name=ranking_info["app_name"],
                                                         bytes_per_user=ranking_info["bytes_per_user"],
                                                         total_bytes=ranking_info["total_bytes"],
                                                         total_devices=ranking_info["total_devices"]))
    except IntegrityError:
        db2.session.rollback()


def insert_or_update_ranking(ranking):
    db_ranking = Ranking.query.filter_by(year=ranking.year, month=ranking.month,
                                         ranking_number=ranking.ranking_number,
                                         carrier_id=ranking.carrier_id,
                                         traffic_type=ranking.traffic_type,
                                         transfer_type=ranking.transfer_type).first()
    if db_ranking is not None:
        db_ranking.total_bytes = ranking.total_bytes
        db_ranking.bytes_per_user = ranking.bytes_per_user
        db_ranking.total_devices = ranking.total_devices
        db_ranking.app_name = ranking.app_name
        db2.session.commit()
    else:
        db2.session.add(ranking)
        db2.session.commit()


# Handles the signal reports (Named signal_report_month_year)
def gsm_signal_import(signals, year, month):
    carriers = Carrier.query.all()
    carrierIds = [c.id for c in carriers]

    try:
        for signal in signals:
            antenna_id = signal["antenna_id"]
            carrier_id = signal["carrier_id"]
            quantity = signal["observations"]
            signal_mean = signal["signal_mean"]
            antenna = Antenna2.query.get(signal["antenna_id"])

            # We ignore the carriers that are not in our database
            if carrier_id not in carrierIds:
                continue

            if not antenna:
                try:
                    ans = get_antenna(antenna_id)
                    if ans == 'Antenna with no lat or lon' or ans is None:
                        continue
                except DifferentIdException:
                    continue

            insert_or_update_signal(GsmSignal(year=year, month=month, antenna_id=antenna_id,
                                                  carrier_id=carrier_id, signal=signal_mean, quantity=quantity))

    except IntegrityError:
        db2.session.rollback()


def insert_or_update_signal(signal):
    try:
        db2.session.add(signal)
        db2.session.commit()
    except IntegrityError:
        db2.session.rollback()
        db_signal = GsmSignal.query.filter_by(year=signal.year, month=signal.month,
                                              carrier_id=signal.carrier_id,
                                              antenna_id=signal.antenna_id).first()
        if db_signal is not None:
            db_signal.quantity = signal.quantity
            db_signal.signal = signal.signal
            db2.session.commit()


def gsm_count_import(counts, year, month):
    carriers = Carrier.query.all()
    carrierIds = [c.id for c in carriers]
    try:
        for count in counts:
            antenna_id = count["antenna_id"]
            carrier_id = count["carrier_id"]
            quantity = count["size"]
            network_type = count["network_type"]
            antenna = Antenna2.query.get(count["antenna_id"])

            if carrier_id not in carrierIds:  # If carrier not in known carriers, we ignore it
                continue

            if not antenna:
                try:
                    ans = get_antenna(antenna_id)
                    if ans == 'Antenna with no lat or lon' or ans is None:
                        continue
                except DifferentIdException:
                    continue

            insert_or_update_gsm_count(GsmCount(year=year, month=month, antenna_id=antenna_id,
                                                    network_type=network_type, carrier_id=carrier_id,
                                                    quantity=quantity))
    except IntegrityError:
        db2.session.rollback()


def insert_or_update_gsm_count(gsm_count):
    try:
        db2.session.add(gsm_count)
        db2.session.commit()
    except IntegrityError:
        db2.session.rollback()
        db_count = GsmCount.query.filter_by(year=gsm_count.year, month=gsm_count.month,
                                            carrier_id=gsm_count.carrier_id,
                                            antenna_id=gsm_count.antenna_id,
                                            network_type=gsm_count.network_type).first()
        if db_count is not None:
            db_count.quantity = gsm_count.quantity
            db2.session.commit()


def get_antenna(an_id):
    with application1.app_context():
        result = Antenna1.query.get(an_id)
    carrier_id = result.carrier_id
    cid = result.cid
    lac = result.lac
    lat = result.lat
    lon = result.lon

    # We add just the antennas that have known lat and lon
    if lat is None or lon is None:
        return 'Antenna with no lat or lon'

    with application2.app_context():
        db2.session.add(Antenna2(id=an_id, cid=cid, lac=lac, lat=lat, lon=lon, carrier_id=carrier_id))

        try:
            db2.session.commit()
        except IntegrityError:
            try:
                db2.session.rollback()
                antenna = Antenna2.query.filter_by(id=an_id).first()
                antenna.lat = lat
                antenna.lon = lon
                db2.session.commit()
            except:
                raise DifferentIdException()
    return Antenna2(id=an_id, cid=cid, lac=lac, lat=lat, lon=lon, carrier_id=carrier_id)


def refresh_materialized_views():
    try:
        sql = 'REFRESH MATERIALIZED VIEW gsm_count_by_carrier'
        db2.engine.execute(sql)
        sql = 'REFRESH MATERIALIZED VIEW gsm_signal_statistic_by_carrier'
        db2.engine.execute(sql)
    except Exception:
        pass


def refresh_antennas_json():
    from app.models_frontend.network_type import NetworkType
    from sqlalchemy import func
    import os
    try:
        carriers = Carrier.query.all()
        carriers = ['0'] + [str(c.id) for c in carriers]
        for carrier in carriers:

            if carrier == '0':
                query = GsmCount.query
            else:
                query = GsmCount.query.filter(GsmCount.carrier_id == carrier)
            result = query.join(NetworkType).join(Antenna2).join(Carrier, Carrier.id == Antenna2.carrier_id).with_entities(
                func.sum(GsmCount.quantity).label('c'),
                GsmCount.antenna_id, NetworkType.type, Carrier.name, Antenna2.lat, Antenna2.lon
            ).group_by(GsmCount.antenna_id, NetworkType.type, Carrier.name, Antenna2.lat, Antenna2.lon).all()

            antennas_data = {}
            antennas_count = 0
            for row in result:
                antenna_id = row.antenna_id
                quantity = row.c
                network_type = row.type
                carrier_name = row.name
                lat = row.lat
                lon = row.lon
                if antenna_id not in antennas_data:
                    antennas_data[antenna_id] = {'lat': lat,
                                                 'lon': lon,
                                                 'carrier': carrier_name,
                                                 '2G': 0,
                                                 '3G': 0,
                                                 '4G': 0,
                                                 'Otras': 0,
                                                 'Total': 0}

                    antennas_count += 1
                antennas_data[antenna_id][network_type] = quantity
                antennas_data[antenna_id]['Total'] += quantity
            antennas_info = {'antennasData': antennas_data,
                             'totalAntennas': antennas_count}
            antennas_dir = "app/static/json/gsm_count/"
            if not os.path.exists(antennas_dir):
                os.makedirs(antennas_dir)
            with open("app/static/json/gsm_count/"+carrier+".json", "w") as jsonfile:
                    json.dump(antennas_info, jsonfile)
    except Exception:
        pass


class DifferentIdException(Exception):
    pass
