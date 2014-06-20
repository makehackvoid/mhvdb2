from mhvdb2 import app
from mhvdb2.models import Entity
import unittest


class test_members(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        # Avoid duplicate email conflicts with other tests
        Entity.drop_table()
        Entity.create_table()

    def valid_test(self, endpoint, valid):
        rv = self.app.post(endpoint, follow_redirects=True, data=valid)
        self.assertEqual(rv.status_code, 200,
                         "Incorrect status code when valid data is submitted")

    # Test that optional fields are optional
    def optional_tests(self, endpoint, valid):
        # No phone number
        data = valid.copy()
        data["phone"] = None
        rv = self.app.post(endpoint, follow_redirects=True, data=data)
        self.assertEqual(rv.status_code, 200,
                         "Incorrect status code when valid data is submitted without phone")

    # Test form validation (required is required, formats checked)
    def validation_tests(self, endpoint, valid):
        # Missing name
        data = valid.copy()
        data["name"] = None
        rv = self.app.post(endpoint, follow_redirects=True, data=data)
        self.assertEqual(rv.status_code, 400,
                         "Incorrect status code when name is missing")

        # Missing email
        data = valid.copy()
        data["email"] = None
        rv = self.app.post(endpoint, follow_redirects=True, data=data)
        self.assertEqual(rv.status_code, 400,
                         "Incorrect status code when email is missing")

        # Invalid email
        data = valid.copy()
        data["email"] = "google.com"
        rv = self.app.post(endpoint, follow_redirects=True, data=data)
        self.assertEqual(rv.status_code, 400,
                         "Incorrect status code when email is malformed")

        # Invalid joined date
        data = valid.copy()
        data["joined_date"] = "not-really-a-date"
        rv = self.app.post(endpoint, follow_redirects=True, data=data)
        self.assertEqual(rv.status_code, 400,
                         "Incorrect status code when joined date is malformed")

        # Invalid agreement date
        data = valid.copy()
        data["agreement_date"] = "not-really-a-date"
        rv = self.app.post(endpoint, follow_redirects=True, data=data)
        self.assertEqual(rv.status_code, 400,
                         "Incorrect status code when agreement date is malformed")

    def test_members_new_get(self):
        rv = self.app.get('/admin/members/new')
        self.assertEqual(rv.status_code, 200,
                         "Incorrect status code when retrieving page")

    def test_members_new_post(self):
        endpoint = '/admin/members/new'
        valid = {
            "name": "Foo Bar",
            "email": "foobar@example.com",
            "phone": "123456789",
            "joined_date": "2014-01-01",
            "agreement_date": "2014-01-01"
        }

        self.valid_test(endpoint, valid)

        rv = self.app.post(endpoint, data=valid)
        self.assertEqual(rv.status_code, 400,
                         "Incorrect status when user with email already exists")

        Entity.delete().where(Entity.email == valid["email"]).execute()
        self.optional_tests(endpoint, valid)
        Entity.delete().where(Entity.email == valid["email"]).execute()
        self.validation_tests(endpoint, valid)

    def test_members_existing_get(self):
        rv = self.app.get('/admin/members/new')
        self.assertEqual(rv.status_code, 200,
                         "Incorrect status code when retrieving page")

    def test_members_existing_post(self):
        valid = {
            "name": "Foo Bar",
            "email": "foobar@example.com",
            "phone": "123456789",
            "joined_date": "2014-01-01",
            "agreement_date": "2014-01-01"
        }

        # Create entity for testing
        member = Entity()
        member.is_member = True
        member.name = valid["name"]
        member.email = valid["email"]
        member.phone = valid["phone"]
        member.joined_date = valid["joined_date"]
        member.agreement_date = valid["agreement_date"]
        member.save()

        endpoint = '/admin/members/{0}'.format(member.id)

        self.valid_test(endpoint, valid)
        self.optional_tests(endpoint, valid)
        self.validation_tests(endpoint, valid)


if __name__ == '__main__':
    unittest.main()
