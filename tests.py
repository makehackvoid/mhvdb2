import os
from mhvdb2 import app
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        #app.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_index(self):
        rv = self.app.get('/')
        self.assertTrue(rv.status_code == 200)

    def test_signup_get(self):
        rv = self.app.get('/signup/')
        self.assertTrue(rv.status_code == 200)

    def test_signup_post(self):
        rv = self.app.post('/signup/', data={
            "first-name": "Foobar",
            "last-name": "foobar",
            "email": "foobar@example.com",
            "phone": "123456789"}
            , follow_redirects = True)

        self.assertTrue(rv.status_code == 200)

        # Invalid email, should return invalid
        rv = self.app.post('/signup/', data={
            "first-name": "Foobar",
            "last-name": "foobar",
            "email": "foobar",
            "phone": "123456789"}
            , follow_redirects = True)

        self.assertTrue(rv.status_code == 400)

        rv = self.app.post('/signup/', follow_redirects = True)
        self.assertTrue(rv.status_code == 400)

if __name__ == '__main__':
    unittest.main()

