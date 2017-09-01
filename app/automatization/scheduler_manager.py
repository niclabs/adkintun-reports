from datetime import datetime

from uwsgidecorators import cron

from app import reportLogger
from app.automatization import monthly_update

MAX_NUMBER_OF_QUERIES = 40


# Job will be done the first day of every month
@cron(0, 0, 1, -1, -1, target="mule")
def reports_generation(num: int):
    """
    Job updating frontend database and generating reports.
    :param num: singal num
    :return:
    """
    monthly_update()
    reportLogger.info(datetime.now().strftime("Reports has been generated. - %H:%M %d/%m/%Y"))