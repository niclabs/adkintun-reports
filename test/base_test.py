import unittest
from app import db1, db2, application1, application2


class BaseTest(unittest.TestCase):

    def setUp(self):
        application1.config.from_object('config.TestConfigServer')
        application2.config.from_object('config.TestConfigFrontend')
        db1.drop_all()
        db1.create_all()

        db2.drop_all()
        db2.create_all()

    def tearDown(self):
        db1.drop_all()
        db2.drop_all()
