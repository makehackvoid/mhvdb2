from mhvdb2 import app
import unittest


class test_entity(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_entity_new_get(self):
        rv = self.app.get('/admin/entities/new', follow_redirects=True)
        self.assertEqual(rv.status_code, 200,
                         "Incorrect status code when retrieving page")

    def test_entity_new_post(self):
        endpoint = '/admin/entities/new'
        valid = {
            "name": "Testing entity",
            "email": "test@example.com",
            "phone": "01189998219991197253"
        }

        rv = self.app.post(endpoint, follow_redirects=True, data=valid)
        self.assertEqual(rv.status_code, 200,
                         "Incorrect status code when valid data is submitted")

        # No phone number
        data = valid.copy()
        data["phone"] = None
        rv = self.app.post(endpoint, follow_redirects=True, data=data)
        self.assertEqual(rv.status_code, 200,
                         "Incorrect status code when valid data is submitted without phone")

        # No email address
        data = valid.copy()
        data["email"] = None
        rv = self.app.post(endpoint, follow_redirects=True, data=data)
        self.assertEqual(rv.status_code, 200,
                         "Incorrect status code when valid data is submitted without email")

        # Missing name
        data = valid.copy()
        data["name"] = None
        rv = self.app.post(endpoint, follow_redirects=True, data=data)
        self.assertEqual(rv.status_code, 400,
                         "Incorrect status code when name is missing")

        # Invalid email
        data = valid.copy()
        data["email"] = "google.com"
        rv = self.app.post(endpoint, follow_redirects=True, data=data)
        self.assertEqual(rv.status_code, 400,
                         "Incorrect status code when email is malformed")

    def test_entity_get(self):
        rv = self.app.get('/admin/entities/1', follow_redirects=True)
        self.assertEqual(rv.status_code, 200,
                         "Incorrect status code when retrieving page")

    def test_entity_post(self):
        endpoint = '/admin/entities/1'
        valid = {
            "name": "Testing entity update",
            "email": "updated@example.com",
            "phone": "12345"
        }

        rv = self.app.post(endpoint, follow_redirects=True, data=valid)
        self.assertEqual(rv.status_code, 200,
                         "Incorrect status code when valid data is submitted")

        # No phone number
        data = valid.copy()
        data["phone"] = None
        rv = self.app.post(endpoint, follow_redirects=True, data=data)
        self.assertEqual(rv.status_code, 200,
                         "Incorrect status code when valid data is submitted without phone")

        # No email address
        data = valid.copy()
        data["email"] = None
        rv = self.app.post(endpoint, follow_redirects=True, data=data)
        self.assertEqual(rv.status_code, 200,
                         "Incorrect status code when valid data is submitted without email")

        # Missing name
        data = valid.copy()
        data["name"] = None
        rv = self.app.post(endpoint, follow_redirects=True, data=data)
        self.assertEqual(rv.status_code, 400,
                         "Incorrect status code when name is missing")

        # Invalid email
        data = valid.copy()
        data["email"] = "google.com"
        rv = self.app.post(endpoint, follow_redirects=True, data=data)
        self.assertEqual(rv.status_code, 400,
                         "Incorrect status code when email is malformed")


if __name__ == '__main__':
    unittest.main()
