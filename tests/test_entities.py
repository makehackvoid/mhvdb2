from mhvdb2.resources import entities
from mhvdb2.models import Entity
import unittest


class EntitiesTestCases(unittest.TestCase):
    def setUp(self):
        self.test_entity = Entity()
        self.test_entity.is_member = False
        self.test_entity.name = "Jane Smith"
        self.test_entity.email = "jane@example.com"
        self.test_entity.phone = "+61 (02) 1234 5678"
        self.test_entity.is_keyholder = False
        self.test_entity.save()

    def tearDown(self):
        self.test_entity.delete_instance()

    def test_get(self):
        entity = entities.get(self.test_entity.id)
        self.assertEqual(entity, self.test_entity)

    def test_get_bad_id(self):
        entity = entities.get(12345)
        self.assertIsNone(entity)

    def test_validate(self):
        errors = entities.validate(self.test_entity.name,
                                   self.test_entity.email,
                                   self.test_entity.phone)
        self.assertEqual(len(errors), 0)

    def test_validate_name(self):
        errors = entities.validate("",
                                   self.test_entity.email,
                                   self.test_entity.phone)
        self.assertEqual(len(errors), 1)

    def test_validate_email(self):
        errors = entities.validate(self.test_entity.name,
                                   "",
                                   self.test_entity.phone)
        self.assertEqual(len(errors), 0)

        errors = entities.validate(self.test_entity.name,
                                   "not-an-email.com",
                                   self.test_entity.phone)
        self.assertEqual(len(errors), 1)

        errors = entities.validate(self.test_entity.name,
                                   "not-an-email@",
                                   self.test_entity.phone)
        self.assertEqual(len(errors), 1)

    def test_validate_phone(self):
        errors = entities.validate(self.test_entity.name,
                                   self.test_entity.email,
                                   "")
        self.assertEqual(len(errors), 0)

    def test_create(self):
        entity_id = entities.create(self.test_entity.name,
                                    self.test_entity.email,
                                    self.test_entity.phone)
        entity = Entity.get(Entity.id == entity_id)

        self.assertNotEqual(entity.id, self.test_entity.id)
        self.assertEqual(entity.name, self.test_entity.name)
        self.assertEqual(entity.email, self.test_entity.email)
        self.assertEqual(entity.phone, self.test_entity.phone)
        entity.delete_instance()

    def test_update(self):
        new_name = "Joe Flanders"
        new_email = "joe@example.com"
        new_phone = "(04) 9876 5432"
        entities.update(self.test_entity.id,
                        new_name,
                        new_email,
                        new_phone)
        entity = Entity.get(Entity.id == self.test_entity.id)
        self.assertEqual(entity.name, new_name)
        self.assertEqual(entity.email, new_email)
        self.assertEqual(entity.phone, new_phone)

if __name__ == '__main__':
    unittest.main()
