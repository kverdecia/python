import os

from sqlalchemy.exc import IntegrityError

from utils import BASE_DIR, TestCase
from bankar_api import StateModel, UserModel


class TestStateModel(TestCase):
    def setUp(self):
        super().setUp()
        self.state_csv_path = os.path.join(BASE_DIR, 'states.csv')

    def test_import_states(self):
        """Test states can be imported correctly."""
        with open(self.state_csv_path) as states_stream:
            StateModel.import_csv(states_stream)
        with open(self.state_csv_path) as states_stream:
            states_stream.readline()
            self.assertEqual(len(states_stream.readlines()), 25)

    def test_import_repeated_states(self):
        """Test importing twice doesn't throw an exception."""
        # import the states
        with open(self.state_csv_path) as states_stream:
            StateModel.import_csv(states_stream)
        # repeat the states
        with open(self.state_csv_path) as states_stream:
            StateModel.import_csv(states_stream)


class TestUserModel(TestCase):
    def setUp(self):
        super().setUp()
        self.state = StateModel(code=1, name="State 1")
        self.state.save()

    def test_create_user(self):
        user = UserModel(name="user1", age=35, state=self.state)
        user.save()
        user.delete()

    def test_create_user_unique_name(self):
        user = UserModel(name="user1", age=35, state=self.state)
        user.save()
        user2 = UserModel(name="user1", age=35, state=self.state)
        self.assertRaises(IntegrityError, user2.save)

    def test_create_user_without_state(self):
        user = UserModel(name="user1", age=35)
        self.assertRaises(IntegrityError, user.save)


