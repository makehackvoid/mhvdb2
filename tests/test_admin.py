from mhvdb2 import app
import unittest


class test_admin(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_admin_get(self):
        rv = self.app.get('/admin/')
        self.assertEqual(rv.status_code, 200,
                         "Incorrect status code when retrieving page")


if __name__ == '__main__':
    unittest.main()
