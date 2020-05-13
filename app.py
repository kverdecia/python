import sys
import os

from flask import Flask
from flask_migrate import Migrate

from config import Config
from bankar_api import db, BankarApi


def create_app(testing=False):
    app = Flask(__name__)
    Config(app, testing)
    register_models(app)
    BankarApi(app)
    return app


def register_models(app):
    db.init_app(app)
    Migrate(app, db)
