from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config1, Config2

application1 = Flask(__name__)
application1.config.from_object(Config1)
db1 = SQLAlchemy(application1)

application2 = Flask(__name__)
application2.config.from_object(Config2)
db2 = SQLAlchemy(application2)
