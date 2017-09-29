from datetime import datetime, timedelta
from app import reportLogger
from app.report.json_generation import save_json_report_to_file

from app.report import general_report
from app.report import app_report
from app.report import signal_strength_mean_for_antenna
from app.report import network_report_for_carrier

from app.importation import report_import
from app.importation import ranking_import
from app.importation import gsm_signal_import
from app.importation import gsm_count_import
from app.importation import refresh_materialized_views
from app.importation import refresh_antennas_json


def monthly_update(month=None, year=None):
    """
    Method to be run at the start of every month.
    :return:
    """
    reports = monthly_reports_generation(month, year)
    monthly_import(reports, month, year)


def monthly_import(reports, month=None, year=None):
    """
    Receives the four reports as an array and tries to insert
    them into the frontend database.
    :param reports: An array containing reports as dictionaries.
    :param month: Month number (1-12)
    :param year: Year number, four digits.
    :return:
    """
    if not month or not year:
        actual_month = datetime.now().month
        actual_year = datetime.now().year
        month_new_import = actual_month - 1
        year_new_import = actual_year

        if month_new_import == 0:
            month_new_import = 12
            year_new_import = year_new_import - 1

        year = year_new_import
        month = month_new_import

    report_import(reports[0], year, month)
    ranking_import(reports[1], year, month)
    gsm_signal_import(reports[2], year, month)
    gsm_count_import(reports[3], year, month)

    refresh_materialized_views()
    refresh_antennas_json()


def monthly_reports_generation(month=None, year=None):
    """
    Generates four reports in a dictionary format and
    saves them as json files.
    :param month: Month number (1-12)
    :param year: Year number, four digits.
    :return: Array containing the reports.
    """
    # get month for the report, not added month or year
    if not month or not year:
        final_month = datetime.now().month
        final_year = datetime.now().year
        month_new_report = final_month - 1
        year_new_report = final_year
        if month_new_report == 0:
            month_new_report = 12
            year_new_report = year_new_report - 1
    else:
        year_new_report = int(year)
        month_new_report = int(month)
        final_month = month_new_report + 1
        final_year = year_new_report
        if final_month == 13:
            final_month = 1
            final_year = year_new_report + 1

    # select limit dates of the selected month
    init_date = datetime(year=year_new_report, month=month_new_report, day=1)
    last_date = datetime(year=final_year, month=final_month, day=1, hour=23, minute=59, second=59) - timedelta(days=1)

    general = None
    app = None
    signal = None
    network = None

    try:
        reportLogger.info("Starting general report generation.")
        general = general_report(init_date, last_date)
        save_json_report_to_file(general, init_date.year, init_date.month, 'general_report_')
        reportLogger.info("General report for {}/{} has been generated".format(month_new_report, year_new_report))
    except Exception as e:
        reportLogger.info("General report generation failed:" + str(e))

    try:
        reportLogger.info("Starting signal report generation.")
        signal = signal_strength_mean_for_antenna(init_date, last_date)
        save_json_report_to_file(signal, init_date.year, init_date.month, 'signal_report_')
        reportLogger.info("Signal report for {}/{} has been generated".format(month_new_report, year_new_report))
    except Exception as e:
        reportLogger.info("Signal report generation failed:" + str(e))

    try:
        reportLogger.info("Starting network report generation.")
        network = network_report_for_carrier(init_date, last_date)
        save_json_report_to_file(network, init_date.year, init_date.month, 'network_report_')
        reportLogger.info("Network report for {}/{} has been generated".format(month_new_report, year_new_report))
    except Exception as e:
        reportLogger.info("Network report generation failed:" + str(e))

    try:
        reportLogger.info("Starting app report generation.")
        app = app_report(init_date, last_date)
        save_json_report_to_file(app, init_date.year, init_date.month, 'apps_report_')
        reportLogger.info("Apps report for {}/{} has been generated".format(month_new_report, year_new_report))
    except Exception as e:
        reportLogger.info("Apps report generation failed:" + str(e))

    return [general, app, signal, network]
