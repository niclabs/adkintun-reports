class Config(object):
    USER = "testuser"
    SECRET_KEY = "testpassword123"
    SQLALCHEMY_DATABASE_URI = "postgresql://" + USER + ":" + SECRET_KEY + "@localhost/nothing"
    SQLALCHEMY_BINDS = {
        "frontend": "postgresql://" + USER + ":" + SECRET_KEY + "@localhost/everything"
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ServerSettings:
    urls = {
    "server_url": "this-should-be-changed",
    "antenna_url" : "antenna",
    "report_url" : "reports",
    "ranking_url" : "reports",
    "network_url" : "reports",
    "signal_url" : "reports"
    }
