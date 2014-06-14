from mhvdb2.models import Payment
import re
from datetime import datetime


def validate(amount, email, method, type, notes, reference):
    flashes = []

    if not amount or not amount.isdigit() or int(amount) <= 0:
        flashes.append("Sorry, you need to provide a valid amount.")
    if not re.match("[^@\s]+@[^@\s]+", email):
        flashes.append("Sorry, you need to provide a valid email address.")
    if not type or not type.isdigit() or int(type) > 2:
        flashes.append("Sorry, you need to provide a valid payment type.")
    if not method or not method.isdigit() or int(method) > 2:
        flashes.append("Sorry, you need to provide a valid payment method.")
    if not reference:
        flashes.append("Sorry, you need to provide a reference.")

    return flashes


def create(amount, entity, method, type, notes, reference):

    # Create payment
    payment = Payment()
    payment.time = datetime.now()
    payment.entity = entity
    payment.amount = amount
    payment.source = method
    payment.is_donation = type != 0
    payment.notes = notes
    if method == 0:  # Bank transfer
        payment.bank_reference = reference
    payment.pending = True
    payment.save()
