from mhvdb2.models import Entity
import re
from datetime import date


def validate(name, email, phone):
    errors = []
    if not name:
        errors.append("Sorry, you need to provide a name.")
    if not email or not re.match("[^@\s]+@[^@\s]+", email):
        errors.append("Sorry, you need to provide an email address.")

    return errors


def create(name, email, phone):
    member = Entity()
    member.is_member = True
    member.joined_date = date.today()
    member.name = name
    member.email = email
    member.phone = phone
    member.agreement_date = date.today()

    return member.save()


# Update via email or member object
def update(name, email, phone, member=None):
    if member is None:
        member = Entity.get(Entity.email == email)
    member.name = name
    member.email = email
    member.phone = phone
    member.agreement_date = date.today()

    return member.save()
