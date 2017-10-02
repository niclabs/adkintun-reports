import unittest
from app import db1, db2, application
from config import DefaultConfig


class BaseTest(unittest.TestCase):

    def setUp(self):
        application.config.from_object('config.TestConfig')
        db1.drop_all()
        db1.create_all()

        db2.drop_all(bind=DefaultConfig.BIND_KEY)
        db2.create_all(bind=DefaultConfig.BIND_KEY)

    def tearDown(self):
        db1.drop_all()
        db2.drop_all(bind=DefaultConfig.BIND_KEY)
        pass
