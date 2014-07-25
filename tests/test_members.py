from mhvdb2.resources import members
from mhvdb2.models import Entity
from datetime import date, timedelta
import unittest


class MembersTestCases(unittest.TestCase):
    def setUp(self):
        self.test_member = Entity()
        self.test_member.is_member = True
        self.test_member.name = "Jane Smith"
        self.test_member.email = "jane@example.com"
        self.test_member.phone = "+61 (02) 1234 5678"
        self.test_member.joined_date = date.today()-timedelta(days=1)
        self.test_member.agreement_date = date.today()
        self.test_member.is_keyholder = False
        self.test_member.save()
        self.joined_date = "2014-12-24"
        self.agreement_date = "2014-12-25"

    def tearDown(self):
        self.test_member.delete_instance()

    def test_get(self):
        member = members.get(self.test_member.id)
        self.assertEqual(member, self.test_member)

    def test_get_bad_id(self):
        member = members.get(12345)
        self.assertIsNone(member)

    def test_validate(self):
        errors = members.validate(self.test_member.name,
                                  self.test_member.email,
                                  self.test_member.phone,
                                  self.joined_date,
                                  self.agreement_date,
                                  self.test_member.is_keyholder)
        self.assertEqual(len(errors), 0)

    def test_validate_name(self):
        errors = members.validate("",
                                  self.test_member.email,
                                  self.test_member.phone,
                                  self.joined_date,
                                  self.agreement_date,
                                  self.test_member.is_keyholder)
        self.assertEqual(len(errors), 1)

    def test_validate_email(self):
        errors = members.validate(self.test_member.name,
                                  "",
                                  self.test_member.phone,
                                  self.joined_date,
                                  self.agreement_date,
                                  self.test_member.is_keyholder)
        self.assertEqual(len(errors), 1)

        errors = members.validate(self.test_member.name,
                                  "not-an-email.com",
                                  self.test_member.phone,
                                  self.joined_date,
                                  self.agreement_date,
                                  self.test_member.is_keyholder)
        self.assertEqual(len(errors), 1)

        errors = members.validate(self.test_member.name,
                                  "not-an-email@",
                                  self.test_member.phone,
                                  self.joined_date,
                                  self.agreement_date,
                                  self.test_member.is_keyholder)
        self.assertEqual(len(errors), 1)

    def test_validate_phone(self):
        errors = members.validate(self.test_member.name,
                                  self.test_member.email,
                                  "",
                                  self.joined_date,
                                  self.agreement_date,
                                  self.test_member.is_keyholder)
        self.assertEqual(len(errors), 0)

    def test_validate_joined_date(self):
        errors = members.validate(self.test_member.name,
                                  self.test_member.email,
                                  self.test_member.phone,
                                  "2014-12-25",
                                  self.agreement_date,
                                  self.test_member.is_keyholder)
        print(errors)
        self.assertEqual(len(errors), 0)

        errors = members.validate(self.test_member.name,
                                  self.test_member.email,
                                  self.test_member.phone,
                                  "The 25th of December, Stardate 21020",
                                  self.agreement_date,
                                  self.test_member.is_keyholder)
        self.assertEqual(len(errors), 1)

    def test_validate_agreement_date(self):
        errors = members.validate(self.test_member.name,
                                  self.test_member.email,
                                  self.test_member.phone,
                                  self.joined_date,
                                  "2014-12-25",
                                  self.test_member.is_keyholder)
        self.assertEqual(len(errors), 0)

        errors = members.validate(self.test_member.name,
                                  self.test_member.email,
                                  self.test_member.phone,
                                  "The 25th of December, Stardate 21020",
                                  self.agreement_date,
                                  self.test_member.is_keyholder)
        self.assertEqual(len(errors), 1)

    def test_create(self):
        member_id = members.create(self.test_member.name,
                                   self.test_member.email,
                                   self.test_member.phone,
                                   self.test_member.joined_date,
                                   self.test_member.agreement_date,
                                   self.test_member.is_keyholder)
        member = Entity.get(Entity.id == member_id)

        self.assertNotEqual(member.id, self.test_member.id)
        self.assertEqual(member.name, self.test_member.name)
        self.assertEqual(member.email, self.test_member.email)
        self.assertEqual(member.phone, self.test_member.phone)
        self.assertEqual(member.joined_date, self.test_member.joined_date)
        self.assertEqual(member.agreement_date, self.test_member.agreement_date)
        self.assertEqual(member.is_keyholder, self.test_member.is_keyholder)
        member.delete_instance()

        member_id = members.create(self.test_member.name,
                                   self.test_member.email,
                                   self.test_member.phone,
                                   None,
                                   self.test_member.agreement_date,
                                   self.test_member.is_keyholder)
        member = Entity.get(Entity.id == member_id)
        self.assertEqual(member.joined_date, date.today())
        member.delete_instance()

        member_id = members.create(self.test_member.name,
                                   self.test_member.email,
                                   self.test_member.phone,
                                   self.test_member.joined_date,
                                   None,
                                   self.test_member.is_keyholder)
        member = Entity.get(Entity.id == member_id)
        self.assertEqual(member.agreement_date, date.today())
        member.delete_instance()

    def test_update(self):
        new_name = "Joe Flanders"
        new_email = "joe@example.com"
        new_phone = "(04) 9876 5432"
        new_joined_date = date.today()-timedelta(days=7)
        new_agreement_date = date.today()-timedelta(days=6)
        new_is_keyholder = True
        members.update(self.test_member.id,
                       new_name,
                       new_email,
                       new_phone,
                       new_joined_date,
                       new_agreement_date,
                       new_is_keyholder)
        member = Entity.get(Entity.id == self.test_member.id)
        self.assertEqual(member.name, new_name)
        self.assertEqual(member.email, new_email)
        self.assertEqual(member.phone, new_phone)
        self.assertEqual(member.joined_date, new_joined_date)
        self.assertEqual(member.agreement_date, new_agreement_date)
        self.assertEqual(member.is_keyholder, new_is_keyholder)

if __name__ == '__main__':
    unittest.main()
