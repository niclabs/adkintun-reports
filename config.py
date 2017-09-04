class DefaultConfig(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "this-should-be-changed"
    USER = "this-should-be-changed"
    HOST = "this-should-be-changed"
    DB_NAME = "this-should-be-changed"
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}/{}".format(USER, SECRET_KEY, HOST, DB_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestConfig(object):
    USER = "testuser"
    SECRET_KEY = "testpassword123"
    SQLALCHEMY_DATABASE_URI = "postgresql://" + USER + ":" + SECRET_KEY + "@localhost/nothing"
    SQLALCHEMY_BINDS = {
        'everything': "postgresql://" + USER + ":" + SECRET_KEY + "@localhost/everything"
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    TESTING = True
    DEBUG = True


class Files:
    STATIC_FILES_FOLDER = "app/static"
    REPORTS_FOLDER = STATIC_FILES_FOLDER + "/" + "reports"
    LOGS_FOLDER = "tmp"
    REPORTS_LOG_FILE = "report.log"
