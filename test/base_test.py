import unittest
from app import db1, db2


class BaseTest(unittest.TestCase):

    def setUp(self):
        db1.drop_all()
        db1.create_all()

        db2.drop_all()
        db2.create_all()

    def tearDown(self):
        db1.drop_all()
        db2.drop_all()
