from app import db1
from app.models_server import utils


class BaseModel(db1.Model):
    '''
    Clase modelo base.
    '''
    __abstract__ = True

    @property
    def dict(self):
        return utils.to_dict(self, self.__class__)
