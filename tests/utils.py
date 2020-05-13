import sys
import os
import urllib.parse

from flask_testing import TestCase as BaseTestCase

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from app import create_app
from bankar_api import db


class TestCase(BaseTestCase):
    "Configure test cases for testing flask sqlalchemy models"

    def create_app(self):
        return create_app(testing=True)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
