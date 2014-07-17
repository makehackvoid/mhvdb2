from mhvdb2.resources import payments, entities
from mhvdb2.models import Payment, Entity
import unittest


class PaymentsTestCases(unittest.TestCase):
    def setUp(self):
        self.type = 2
        self.email = "jane@example.com"
        self.entity = Entity.get(Entity.id == entities.create("Jane Doe", self.email, ""))
        self.amount = 1234
        self.entity = self.entity
        self.method = 0
        self.is_donation = True
        self.notes = "For services rendered"
        self.reference = "yx92s3"

    def tearDown(self):
        self.entity.delete_instance()

    def test_validate(self):
        errors = payments.validate(str(self.amount),
                                   self.email,
                                   str(self.method),
                                   str(self.type),
                                   self.notes,
                                   self.reference)
        self.assertEqual(len(errors), 0)

    def test_validate_amount(self):
        errors = payments.validate("-100",
                                   self.email,
                                   str(self.method),
                                   str(self.type),
                                   self.notes,
                                   self.reference)
        self.assertEqual(len(errors), 1)

    def test_validate_email(self):
        errors = payments.validate(str(self.amount),
                                   "",
                                   str(self.method),
                                   str(self.type),
                                   self.notes,
                                   self.reference)
        self.assertEqual(len(errors), 1)

        errors = payments.validate(str(self.amount),
                                  "not-an-email.com",
                                   str(self.method),
                                   str(self.type),
                                   self.notes,
                                   self.reference)
        self.assertEqual(len(errors), 1)

        errors = payments.validate(str(self.amount),
                                  "not-an-email@",
                                   str(self.method),
                                   str(self.type),
                                   self.notes,
                                   self.reference)
        self.assertEqual(len(errors), 1)

    def test_validate_method(self):
        errors = payments.validate(str(self.amount),
                                   self.email,
                                   "1",
                                   str(self.type),
                                   self.notes,
                                   self.reference)
        self.assertEqual(len(errors), 1)

    def test_validate_type(self):
        errors = payments.validate(str(self.amount),
                                   self.email,
                                   str(self.method),
                                   "3",
                                   self.notes,
                                   self.reference)
        self.assertEqual(len(errors), 1)

    def test_validate_notes(self):
        errors = payments.validate(str(self.amount),
                                   self.email,
                                   str(self.method),
                                   str(self.type),
                                   "",
                                   self.reference)
        self.assertEqual(len(errors), 0)

    def test_validate_reference(self):
        errors = payments.validate(str(self.amount),
                                   self.email,
                                   str(self.method),
                                   str(self.type),
                                   self.notes,
                                   "")
        self.assertEqual(len(errors), 1)

    def test_create(self):
        payment_id = payments.create(str(self.amount),
                                     self.email,
                                     self.method,
                                     self.type,
                                     self.notes,
                                     self.reference)
        payment = Payment.get(Payment.id == payment_id)

        self.assertNotEqual(payment.id, self.id)
        self.assertEqual(payment.amount, self.amount)
        self.assertEqual(payment.entity.id, self.entity.id)
        self.assertEqual(payment.source, self.method)
        self.assertEqual(payment.is_donation, self.is_donation)
        self.assertEqual(payment.notes, self.notes)
        self.assertEqual(payment.bank_reference, self.reference)
        payment.delete_instance()

if __name__ == '__main__':
    unittest.main()
