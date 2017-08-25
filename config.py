class DefaultConfigServer(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "this-really-needs-to-be-changed"
    USER = "this-really-needs-to-be-changed"
    SQLALCHEMY_DATABASE_URI = "postgresql://" + USER + ":" + SECRET_KEY + "@localhost/this-really-needs-to-be-changed"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DefaultConfigFrontend(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "this-should-be-changed"
    USER = "this-should-be-changed"
    HOST = "this-should-be-changed"
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}/visualization".format(USER, SECRET_KEY, HOST)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    CORS_DOMAIN = 'this-should-be-changed'  # Set to visualization server ip or '*' for all


class TestConfigServer(object):
    USER = "testuser"
    SECRET_KEY = "testpassword123"
    SQLALCHEMY_DATABASE_URI = "postgresql://" + USER + ":" + SECRET_KEY + "@localhost/nothing"
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    TESTING = True
    DEBUG = True


class TestConfigFrontend(object):
    USER = "testuser"
    SECRET_KEY = "testpassword123"
    SQLALCHEMY_DATABASE_URI = "postgresql://" + USER + ":" + SECRET_KEY + "@localhost/everything"
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    TESTING = True
    DEBUG = True


class Files:
    STATIC_FILES_FOLDER = "app/static"
    REPORTS_FOLDER = STATIC_FILES_FOLDER + "/" + "reports"
    LOGS_FOLDER = "tmp"
    REPORTS_LOG_FILE = "report.log"
