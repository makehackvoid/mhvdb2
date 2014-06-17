from mhvdb2 import app
import unittest


class test_payment(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

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
        data["notes"] = None
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
        data["reference"] = None
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

if __name__ == '__main__':
    unittest.main()
