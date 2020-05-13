from flask_restful import Api
from .resources import StateListResource, UserListResource, UserResource


class BankarApi:
    def __init__(self, app):
        self.app = app
        self.api = Api(app)
        self.api.add_resource(StateListResource, '/api/v1/states')
        self.api.add_resource(UserListResource, '/api/v1/users')
        self.api.add_resource(UserResource, '/api/v1/users/<int:user_id>')
