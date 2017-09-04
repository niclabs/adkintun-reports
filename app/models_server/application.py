from app import db1, application
from app.models_server import base_model


class Application(base_model.BaseModel):
    """
    Android Apps model class
    """
    __tablename__ = "applications"
    id = db1.Column(db1.Integer, primary_key=True)
    package_name = db1.Column(db1.String(100), unique=True)
    application_traffic_event = db1.relationship("ApplicationTrafficEvent", backref="application", lazy="dynamic")

    def __init__(self, package_name=None):
        self.package_name = package_name

    def __repr__(self):
        return "<Application, package_name: %r, id: %r>" % (self.package_name, self.id)

    @staticmethod
    def get_app_or_add_it(package_name: str):
        """
        Search an app and retrieve it if exist, else create a new one and retrieve it.
        :param package_name: name of the application package
        :return: App object
        """
        app = Application.query.filter(Application.package_name == package_name).first()
        if not app:
            app = Application(package_name=package_name)
            db1.session.add(app)
            try:
                db1.session.commit()
            except Exception as e:
                db1.session.rollback()
                application.logger.error(
                    "Error adding application to database, package_name:" + package_name + " - " + str(e))
        return app
