from flask import request
from flask_restful import Resource, Api

from .models import StateModel, UserModel
from .forms import CreateUserForm, UpdateUserForm


class StateListResource(Resource):
    def get(self):
        return [state.get_data() for state in StateModel.query.all()]


class UserListResource(Resource):
    def get(self):
        return [user.get_data() for user in UserModel.query.all()]

    def post(self):
        form = CreateUserForm(request.form)
        if form.validate():
            state = StateModel.get_by_code(form.state_id.data)
            user = UserModel(name=form.name.data, age=form.age.data, state=state)
            user.save()
            return dict(ok=True, user=user.get_data()), 201
        return dict(ok=False, user=None, error="validation_error"), 421


class UserResource(Resource):
    def get(self, user_id):
        user = UserModel.get_by_id(user_id)
        if user is None:
            return dict(error="user_not_found"), 404
        return user.get_data()

    def patch(self, user_id):
        user = UserModel.get_by_id(user_id)
        if user is None:
            return dict(error="user_not_found"), 404
        form = UpdateUserForm(user, request.form)
        if form.validate():
            form.populate_obj(user)
            user.save()
            return dict(ok=True, user=user.get_data()), 200
        return dict(ok=False, user=user.get_data(), error="validation_error"), 421

    def delete(self, user_id):
        user = UserModel.get_by_id(user_id)
        if user is None:
            return dict(ok=False, error="user_not_found"), 404
        user.delete()
        return '', 204
