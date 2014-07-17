from mhvdb2 import app
from mhvdb2 import authentication
from mhvdb2.authentication import User
import unittest


class AuthenticationTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.name = "Joe Bloggs"
        self.email = "joe@example.com"
        self.password = "123abc"
        print(User.delete().where(User.email == self.email).execute())

    def test_register(self):
        errors = authentication.register_user(self.name, self.email, self.password)
        user = User.get(User.email == self.email)
        self.assertEqual(len(errors), 0)
        self.assertEqual(user.name, self.name)
        self.assertEqual(user.email, self.email)

    def test_register_no_name(self):
        errors = authentication.register_user("", self.email, self.password)
        self.assertEqual(len(errors), 1)

    def test_register_no_email(self):
        errors = authentication.register_user(self.name, "", self.password)
        self.assertEqual(len(errors), 1)

    def test_register_bad_password(self):
        errors = authentication.register_user(self.name, self.email, "")
        self.assertEqual(len(errors), 1)

        errors = authentication.register_user(self.name, self.email, "12345")
        self.assertEqual(len(errors), 1)

    def test_authenticate_user(self):
        with app.test_request_context():
            authentication.register_user(self.name, self.email, self.password)
            self.assertTrue(authentication.authenticate_user(self.email, self.password))
            self.assertFalse(authentication.authenticate_user(self.email, "abc123"))
            self.assertFalse(authentication.authenticate_user("jane@example.com", self.password))
            User.delete().where(User.email == self.email)


if __name__ == '__main__':
    unittest.main()
