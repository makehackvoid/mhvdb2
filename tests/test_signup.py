from mhvdb2 import app
import unittest


class test_signup(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_signup_get(self):
        rv = self.app.get('/signup/')
        self.assertEqual(rv.status_code, 200,
                         "Incorrect status code when retrieving page")

    def test_signup_post(self):
        endpoint = '/signup/'
        valid = {
            "name": "Foo Bar",
            "email": "foobar@example.com",
            "phone": "123456789",
            "agree": "true"
        }

        rv = self.app.post(endpoint, data=valid)
        self.assertEqual(rv.status_code, 200,
                         "Incorrect status code when valid data is submitted")

        # No phone number
        data = valid.copy()
        data["phone"] = None
        rv = self.app.post(endpoint, data=data)
        self.assertEqual(rv.status_code, 200,
                         "Incorrect status code when valid data is submitted without phone")

        # Missing name
        data = valid.copy()
        data["name"] = None
        rv = self.app.post(endpoint, data=data)
        self.assertEqual(rv.status_code, 400,
                         "Incorrect status code when name is missing")

        # Missing email
        data = valid.copy()
        data["email"] = None
        rv = self.app.post(endpoint, data=data)
        self.assertEqual(rv.status_code, 400,
                         "Incorrect status code when email is missing")

        # Missing agreement
        data = valid.copy()
        data["agree"] = None
        rv = self.app.post(endpoint, data=data)
        self.assertEqual(rv.status_code, 400,
                         "Incorrect status code when user doesn't agree")

        # Invalid email
        data = valid.copy()
        data["email"] = "google.com"
        rv = self.app.post(endpoint, data=data)
        self.assertEqual(rv.status_code, 400,
                         "Incorrect status code when email is malformed")


if __name__ == '__main__':
    unittest.main()
