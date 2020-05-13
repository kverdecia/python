from wtforms import Form, IntegerField, StringField, validators
from .models import StateModel, UserModel


class BaseUserForm(Form):
    name = StringField('Name', [validators.InputRequired(), validators.Length(min=2, max=80)])
    age = IntegerField('Age', [validators.InputRequired(), validators.NumberRange(min=0, max=100)])
    state_id = IntegerField('Age', [validators.InputRequired(), validators.NumberRange(min=0, max=100)])

    def validate_state_id(self, field):
        state = StateModel.get_by_code(field.data)
        if state is None:
            raise validators.ValidationError("state with id {} don't exist".format(field.data))


class CreateUserForm(BaseUserForm):
    def validate_name(self, field):
        user = UserModel.get_by_name(field.data)
        if user is not None:
            raise validators.ValidationError("There is an user with name: {}".format(field.data))


class UpdateUserForm(BaseUserForm):
    name = StringField('Name', [validators.Length(min=2, max=80)])
    age = IntegerField('Age', [validators.NumberRange(min=0, max=100)])
    state_id = IntegerField('Age', [validators.NumberRange(min=0, max=100)])

    def __init__(self, user_model, *args, **kwargs):
        self.user_model = user_model
        super().__init__(*args, **kwargs)

    def validate_name(self, field):
        user = UserModel.query.filter(UserModel.name==field.data, UserModel.id != self.user_model.id).first()
        if user is not None:
            raise validators.ValidationError("There is an user with name: {}".format(field.data))
