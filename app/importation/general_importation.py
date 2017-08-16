from app import db
from app.models_frontend.carrier import Carrier
from app.models_frontend.report import Report
from app.models_frontend.ranking import Ranking
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
        db.session.rollback()


def insert_or_update_report(report):
    try:
        db.session.add(report)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        db_report = Report.query.filter_by(year=report.year, month=report.month,
                                           carrier_id=report.carrier_id, type=report.type).first()
        if db_report is not None:
            db_report.quantity = report.quantity
            db.session.commit()


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
        db.session.rollback()


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
        db.session.commit()
    else:
        db.session.add(ranking)
        db.session.commit()
