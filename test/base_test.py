import unittest
from app import db


class BaseTest(unittest.TestCase):

    def setUp(self):
        db.drop_all()
        db.create_all()

    def tearDown(self):
        pass
