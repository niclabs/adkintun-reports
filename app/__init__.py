from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_autoindex import AutoIndex

from config import DefaultConfig
from config import Files

import logging
from logging.handlers import RotatingFileHandler
import os

# creates application and both database objects
application = Flask(__name__)
application.config.from_object(DefaultConfig)
db1 = SQLAlchemy(application)
db2 = SQLAlchemy(application)

# creates logger
reportLogger = logging.getLogger(__name__)

log_folder = Files.LOGS_FOLDER
log_filename = Files.REPORTS_LOG_FILE
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

file_handler = RotatingFileHandler(log_folder + "/" + log_filename, maxBytes=50 * 1024 * 1024)
file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"))
reportLogger.setLevel(logging.INFO)
file_handler.setLevel(logging.INFO)
reportLogger.addHandler(file_handler)
reportLogger.info("Report log start")

# Listing reports directory
autoindex = AutoIndex(application, browse_root=Files.REPORTS_FOLDER, add_url_rules=False)

# import views
from app.report import views
from app.public import views

# starts scheduler for monthly update
# start uwsgi cron jobs for monthly update
# Just run in a uwsgi instance!
try:
    import app.automatization.scheduler_manager

    reportLogger.info("Uwsgi mules created for monthly update")
except:
    reportLogger.error("Problem with the mules")
