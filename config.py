class DefaultConfig(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    USER_SERVER = "niclabs"
    SECRET_KEY_SERVER = "niclabs"
    HOST_SERVER = "172.30.65.178"
    DB_NAME_SERVER = "adkintunMobile"
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}/{}".format(USER_SERVER, SECRET_KEY_SERVER,
                                                                HOST_SERVER, DB_NAME_SERVER)
    BIND_KEY = "frontend"
    USER_FRONTEND = "this-should-be-changed"
    SECRET_KEY_FRONTEND = "this-should-be-changed"
    HOST_FRONTEND = "this-should-be-changed"
    DB_NAME_FRONTEND = "this-should-be-changed"
    SQLALCHEMY_BINDS = {
        BIND_KEY: "postgresql://{}:{}@{}/{}".format(USER_FRONTEND, SECRET_KEY_FRONTEND,
                                                    HOST_FRONTEND, DB_NAME_FRONTEND)
    }


class TestConfig(object):
    USER = "testuser"
    SECRET_KEY = "testpassword123"
    BIND_KEY = "frontend"
    SQLALCHEMY_DATABASE_URI = "postgresql://" + USER + ":" + SECRET_KEY + "@localhost/nothing"
    SQLALCHEMY_BINDS = {
        BIND_KEY: "postgresql://" + USER + ":" + SECRET_KEY + "@localhost/everything"
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
