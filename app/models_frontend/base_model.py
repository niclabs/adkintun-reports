from app import db
from app.models_frontend import utils


class BaseModel(db.Model):
    __abstract__ = True

    @property
    def dict(self):
        return utils.to_dict(self, self.__class__)
