from mhvdb2 import app
from mhvdb2.models import Entity
import unittest


class test_signup(unittest.TestCase):
    endpoint = '/signup/'
    data = {
        "name": "Foo Bar",
        "email": "foobar@example.com",
        "phone": "123456789",
        "agree": "true"
    }

    def setUp(self):
        self.app = app.test_client()
        # Avoid duplicate email conflicts with other tests
        Entity.drop_table()
        Entity.create_table()

    def test_signup_get(self):
        rv = self.app.get(self.endpoint)
        self.assertEqual(rv.status_code, 200,
                         "Incorrect status code when retrieving page")

    def test_signup_post_valid(self):
        rv = self.app.post(self.endpoint, data=self.data)
        self.assertEqual(rv.status_code, 200,
                         "Incorrect status code when valid data is submitted")

    def test_signup_post_duplicate(self):
        # Submit twice
        rv = self.app.post(self.endpoint, data=self.data)
        rv = self.app.post(self.endpoint, data=self.data)
        self.assertEqual(rv.status_code, 400,
                         "Incorrect status when user with email already exists")

    def test_signup_post_validation(self):
        # No phone number
        data = self.data.copy()
        data["phone"] = None
        rv = self.app.post(self.endpoint, data=data)
        self.assertEqual(rv.status_code, 200,
                         "Incorrect status code when valid data is submitted without phone")

        # Missing name
        data = self.data.copy()
        data["name"] = None
        rv = self.app.post(self.endpoint, data=data)
        self.assertEqual(rv.status_code, 400,
                         "Incorrect status code when name is missing")

        # Missing email
        data = self.data.copy()
        data["email"] = None
        rv = self.app.post(self.endpoint, data=data)
        self.assertEqual(rv.status_code, 400,
                         "Incorrect status code when email is missing")

        # Missing agreement
        data = self.data.copy()
        data["agree"] = None
        rv = self.app.post(self.endpoint, data=data)
        self.assertEqual(rv.status_code, 400,
                         "Incorrect status code when user doesn't agree")

        # Invalid email
        data = self.data.copy()
        data["email"] = "google.com"
        rv = self.app.post(self.endpoint, data=data)
        self.assertEqual(rv.status_code, 400,
                         "Incorrect status code when email is malformed")


if __name__ == '__main__':
    unittest.main()
