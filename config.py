import os
import urllib.parse


class Config:
    def __init__(self, app, testing=False):
        self.app = app
        self.DEBUG = True
        self.TESTING = testing
        self.SQLALCHEMY_DATABASE_URI = self.get_database_uri()
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        app.config.from_object(self)

    def get_database_uri(self):
        if self.TESTING:
            database_uri = os.environ.get('TEST_DATABASE_URI', 'postgresql+psycopg2://bankar:bankar@db_test/test_bankar')
            parsed = urllib.parse.urlparse(database_uri)
            if not parsed.path.startswith('/test_'):
                raise ValueError("Wrong test configuration: Database name in test database uri must begin with 'test_'")
            return database_uri
        return os.environ.get('DATABASE_URI', 'postgresql+psycopg2://bankar:bankar@db/bankar')
