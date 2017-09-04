from app import db2
from app.models_frontend import utils


class BaseModel(db2.Model):
    __abstract__ = True
    __bind_key__ = "everything"
    @property
    def dict(self):
        return utils.to_dict(self, self.__class__)
