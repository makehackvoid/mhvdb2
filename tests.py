from mhvdb2 import app
import unittest


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_index(self):
        rv = self.app.get('/')
        self.assertTrue(rv.status_code == 200)

    def test_signup_get(self):
        rv = self.app.get('/signup/')
        self.assertTrue(rv.status_code == 200)

    def test_signup_post(self):
        rv = self.app.post('/signup/', data={
            "name": "Foo Bar",
            "email": "foobar@example.com",
            "phone": "123456789"},
            follow_redirects=True)

        self.assertTrue(rv.status_code == 200)

        # Invalid email, should return invalid
        rv = self.app.post('/signup/', data={
            "name": "foobar",
            "email": "foobar",
            "phone": "123456789"},
            follow_redirects=True)

        self.assertTrue(rv.status_code == 400)

        rv = self.app.post('/signup/', follow_redirects=True)
        self.assertTrue(rv.status_code == 400)

    def test_payment_get(self):
        rv = self.app.get('/signup/')
        self.assertTrue(rv.status_code == 200)

    def test_payment_post(self):
        # Make sure there is a signed up user
        rv = self.app.post('/signup/', data={
            "name": "Alice",
            "email": "alice@example.com",
            "phone": "123456789"},
            follow_redirects=True)

        rv = self.app.post('/payments/', data={
            "amount": 12,
            "email": "alice@example.com",
            "method": 0,
            "type": 0,
            "notes": "This is my first payment",
            "reference": "alice"},
            follow_redirects=True)

        self.assertTrue(rv.status_code == 200)

        # Invalid email, should return invalid
        rv = self.app.post('/signup/', data={
            "first-name": "Foobar",
            "last-name": "foobar",
            "email": "foobar",
            "phone": "123456789"},
            follow_redirects=True)

        self.assertTrue(rv.status_code == 400)

        rv = self.app.post('/signup/', follow_redirects=True)
        self.assertTrue(rv.status_code == 400)


if __name__ == '__main__':
    unittest.main()
