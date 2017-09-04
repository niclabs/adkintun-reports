import unittest
from app import db1, db2, application


class BaseTest(unittest.TestCase):

    def setUp(self):
        application.config.from_object('config.TestConfig')
        db1.drop_all()
        db1.create_all()

        db2.drop_all(bind="everything")
        db2.create_all(bind="everything")

    def tearDown(self):
        # db1.drop_all(bind="nothing")
        # db2.drop_all(bind="everything")
        pass
