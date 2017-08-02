import unittest
from app.app import application, db

class BaseTest(unittest.TestCase):

    def setUp(self):
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.drop_all()