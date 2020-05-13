import os

from sqlalchemy.exc import IntegrityError

from utils import BASE_DIR, TestCase
from bankar_api import StateModel, UserModel


class TestStateApi(TestCase):
    def setUp(self):
        super().setUp()
        self.state = StateModel(code=1, name="State 1")
        self.state.save()
        self.state2 = StateModel(code=2, name="State 2")
        self.state2.save()

    def test_state_list(self):
        response = self.client.get('/api/v1/states')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [self.state.get_data(), self.state2.get_data()])


class TestResourceApi(TestCase):
    def setUp(self):
        super().setUp()
        self.state = StateModel(code=1, name="State 1")
        self.state.save()
        self.state2 = StateModel(code=2, name="State 2")
        self.state2.save()

    def test_user_list(self):
        "Test endpoint for listing users"
        user = UserModel(name="User 1", age=20, state=self.state)
        user.save()
        user2 = UserModel(name="User 2", age=30, state=self.state2)
        user.save()
        response = self.client.get('/api/v1/users')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [user.get_data(), user2.get_data()])

    def test_user_create(self):
        "Test endpoint for create a new user"
        self.assertEqual(UserModel.query.count(), 0)
        response = self.client.post('/api/v1/users', data=dict(name="user", age=35, state_id=self.state.code))
        self.assertEqual(UserModel.query.count(), 1)
        user = UserModel.query.first()
        self.assertEqual(user.name, "user")
        self.assertEqual(user.age, 35)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, dict(ok=True, user=user.get_data()))

    def test_user_by_id(self):
        "Test endpoint for returning an user by its id"
        user = UserModel(name="User 1", age=20, state=self.state)
        user.save()
        response = self.client.get('/api/v1/users/{}'.format(user.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, user.get_data())

    def test_user_not_found(self):
        "Test endpoint for returning an user using an unexisting id"
        response = self.client.get('/api/v1/users/3838')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, dict(error='user_not_found'))

    def test_user_delete(self):
        "Test endpoint for deleting users by their ids"
        user = UserModel(name="User 1", age=20, state=self.state)
        user.save()
        self.assertTrue(UserModel.get_by_id(user.id) is not None)
        response = self.client.delete('/api/v1/users/{}'.format(user.id))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, b'')
        self.assertIsNone(UserModel.get_by_id(user.id))

    def test_user_delete_not_found(self):
        "Test endpoint for deleting users with unexisting ids"
        response = self.client.delete('/api/v1/users/3838')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, dict(ok=False, error='user_not_found'))

    def test_user_update(self):
        "Test endpoint for modifying the user with only the name."
        user = UserModel(name="User 1", age=20, state=self.state)
        user.save()

        response = self.client.patch('/api/v1/users/{}'.format(user.id),
            data=dict(name="User (modified)", age=44, state_id=self.state2.code))
        user = UserModel.get_by_id(user.id)
        self.assertEqual(user.name, "User (modified)")
        self.assertEqual(user.age, 44)
        self.assertEqual(user.state_id, self.state2.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, dict(ok=True, user=user.get_data()))

    def test_user_update_not_found(self):
        "Test endpoint for updating users with unexisting ids"
        response = self.client.patch('/api/v1/users/3838', data=dict(name="user", age=55))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, dict(error='user_not_found'))

    def test_user_udate_clash_names(self):
        """Test endpoint for updating an user with the name of
        another existing user"""
        user = UserModel(name="User 1", age=20, state=self.state)
        user.save()
        user2 = UserModel(name="User 2", age=40, state=self.state2)
        user2.save()
        
        response = self.client.patch('/api/v1/users/{}'.format(user.id),
            data=dict(name="User 2"))
        self.assertEqual(response.status_code, 421)
        self.assertEqual(response.json, dict(ok=False, user=user.get_data(), error="validation_error"))
