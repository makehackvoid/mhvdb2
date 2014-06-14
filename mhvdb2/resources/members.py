from mhvdb2.models import Entity
import re
from datetime import date


def validate(name, email, phone):
    flashes = []
    if not name:
        flashes.append("Sorry, you need to provide a name.")
    if not phone:
        flashes.append("Sorry, you need to provide a phone number.")
    if not re.match("[^@\s]+@[^@\s]+", email):
        flashes.append("Sorry, you need to provide an email address.")

    return flashes


def create(name, email, phone):
    member = Entity()
    member.is_member = True
    member.joined_date = date.today()
    member.name = name
    member.email = email
    member.phone = phone
    member.agreement_date = date.today()

    return member.save()


def update(member, name, email, phone):
    member.name = name
    member.email = email
    member.phone = phone
    member.agreement_date = date.today()

    return member.save()
