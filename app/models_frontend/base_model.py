from app import db2
from app.models_frontend import utils
from config import DefaultConfig


class BaseModel(db2.Model):
    __abstract__ = True
    __bind_key__ = DefaultConfig.BIND_KEY
    @property
    def dict(self):
        return utils.to_dict(self, self.__class__)
