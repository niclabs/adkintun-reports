from datetime import datetime

from uwsgidecorators import cron

from app import reportLogger
from app.automatization import monthly_update


# Job will be done the first day of every month
@cron(40, 13, 15, -1, -1, target="mule")
def reports_generation(num: int):
    """
    Job updating frontend database and generating reports.
    :return:
    """
    reportLogger.info(datetime.now().strftime("Monthly update is starting. - %H:%M %d/%m/%Y"))
    monthly_update()
    reportLogger.info(datetime.now().strftime("Monthly update was completed. - %H:%M %d/%m/%Y"))
