from app import db
from app.models_frontend.carrier import Carrier
from app.models_frontend.report import Report

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
