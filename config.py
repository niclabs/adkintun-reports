class Config1(object):
    USER = "testuser"
    SECRET_KEY = "testpassword123"
    SQLALCHEMY_DATABASE_URI = "postgresql://" + USER + ":" + SECRET_KEY + "@localhost/nothing"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Config2(object):
    USER = "testuser"
    SECRET_KEY = "testpassword123"
    SQLALCHEMY_DATABASE_URI = "postgresql://" + USER + ":" + SECRET_KEY + "@localhost/everything"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Files:
    STATIC_FILES_FOLDER = "app/static"
    REPORTS_FOLDER = STATIC_FILES_FOLDER + "/" + "reports"
