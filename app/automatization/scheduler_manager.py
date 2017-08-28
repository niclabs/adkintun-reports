from app.automatization import monthly_update
from apscheduler.schedulers.background import BackgroundScheduler


def start_scheduler():
    scheduler = BackgroundScheduler()
    # every 1st, of every month
    scheduler.add_cron_job(monthly_update, day=1)
    scheduler.start()
