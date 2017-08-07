class Config(object):
    USER = "testuser"
    SECRET_KEY = "testpassword123"
    SQLALCHEMY_DATABASE_URI = "postgresql://" + USER + ":" + SECRET_KEY + "@localhost/nothing"
    SQLALCHEMY_BINDS = {
        "frontend": "postgresql://" + USER + ":" + SECRET_KEY + "@localhost/everything"
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
