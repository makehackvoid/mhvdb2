from mhvdb2 import app
import unittest


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_index(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 200,
                         "Incorrect status code when retrieving page")

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
        data["phone"] = ""
        rv = self.app.post(endpoint, data=data)
        self.assertEqual(rv.status_code, 200,
            "Incorrect status code when valid data is submitted without phone")

        # Missing name
        data = valid.copy()
        data["name"] = ""
        rv = self.app.post(endpoint, data=data)
        self.assertEqual(rv.status_code, 400,
                         "Incorrect status code when name is missing")

        # Missing email
        data = valid.copy()
        data["email"] = ""
        rv = self.app.post(endpoint, data=data)
        self.assertEqual(rv.status_code, 400,
                         "Incorrect status code when email is missing")

        # Missing agreement
        data = valid.copy()
        data["agree"] = ""
        rv = self.app.post(endpoint, data=data)
        self.assertEqual(rv.status_code, 400,
                         "Incorrect status code when user doesn't agree")

        # Invalid email
        data = valid.copy()
        data["email"] = "google.com"
        rv = self.app.post(endpoint, data=data)
        self.assertEqual(rv.status_code, 400,
                         "Incorrect status code when email is malformed")

    def test_payment_get(self):
        rv = self.app.get('/payments/')
        self.assertEqual(rv.status_code, 200,
                         "Incorrect status code when retrieving page")

    def test_payment_post(self):
        # Make sure there is a signed up user
        rv = self.app.post('/signup/', data={
            "name": "Alice",
            "email": "alice@example.com",
            "phone": "123456789",
            "agree": "true"})
        self.assertEqual(rv.status_code, 200)
        #  Don't bother keeping going if our signup failed
        if rv.status_code != 200:
            return

        endpoint = "/payments/"
        valid = {
            "amount": "12",
            "email": "alice@example.com",
            "method": "0",
            "type": "0",
            "notes": "This is my first payment",
            "reference": "alice"
        }

        # Valid baseline
        rv = self.app.post(endpoint, data=valid)
        self.assertEqual(rv.status_code, 200,
                         "Incorrect status code when valid data is submitted")

        # No notes
        data = valid.copy()
        data["notes"] = ""
        rv = self.app.post(endpoint, data=data)
        self.assertEqual(rv.status_code, 200,
                         "Incorrect status code when notes is empty")

        # Invalid email format
        data = valid.copy()
        data["email"] = "not-an-email.com"
        rv = self.app.post(endpoint, data=data)
        self.assertEqual(rv.status_code, 400,
                         "Incorrect status code when email is malformed")

        # Valid email, data member
        data = valid.copy()
        data["email"] = "bob@example.com"
        rv = self.app.post(endpoint, data=data)
        self.assertEqual(rv.status_code, 400,
                         "Incorrect status code when email is not a member")

        # Missing reference
        data = valid.copy()
        data["reference"] = ""
        rv = self.app.post(endpoint, data=data)
        self.assertEqual(rv.status_code, 400,
                         "Incorrect status code when reference is missing")

        # Decimal amount, should be integer cents
        data = valid.copy()
        data["amount"] = "123.45"
        rv = self.app.post(endpoint, data=data)
        self.assertEqual(rv.status_code, 400,
                         "Incorrect status code when amount is a decimal")

        # data method
        data = valid.copy()
        data["method"] = "1"  # Current valid methods: 0
        rv = self.app.post(endpoint, data=data)
        self.assertEqual(rv.status_code, 400,
                         "Incorrect status code on unsupported method")

        # data type
        data = valid.copy()
        data["type"] = "3"  # Current valid types: 0, 1, 2
        rv = self.app.post(endpoint, data=data)
        self.assertEqual(rv.status_code, 400,
                         "Incorrect status code on unsupported type")

    def test_admin_get(self):
        rv = self.app.get('/admin/')
        self.assertEqual(rv.status_code, 200,
                         "Incorrect status code when retrieving page")

if __name__ == '__main__':
    unittest.main()
