from mhvdb2.models import Entity
import re
from datetime import date, datetime, timedelta
from peewee import DoesNotExist
import string
import random

def get(member_id):
    try:
        return Entity.get((Entity.id == member_id) & Entity.is_member)
    except DoesNotExist:
        return None


def exists(email, member_id=None):
    if member_id:
        return Entity.select().where((Entity.email == email) & Entity.is_member,
                                     (Entity.id != member_id)).count() == 1
    else:
        return Entity.select().where((Entity.email == email) & Entity.is_member).count() == 1


def validate(name, email, phone, joined_date=None, agreement_date=None, is_keyholder=None):
    errors = []
    if not name:
        errors.append("Sorry, you need to provide a name.")
    if not email or not re.match("[^@\s]+@[^@\s]+", email):
        errors.append("Sorry, you need to provide an email address.")
    if joined_date:
        try:
            datetime.strptime(joined_date, '%Y-%m-%d')
        except:
            errors.append("Sorry, joined date must be in an acceptable format")
    if agreement_date:
        try:
            datetime.strptime(agreement_date, '%Y-%m-%d')
        except:
            errors.append("Sorry, agreement date must be in an acceptable format")

    return errors


def create(name, email, phone, joined_date=None, agreement_date=None, is_keyholder=None):
    if joined_date is None:
        joined_date = date.today()
    if agreement_date is None:
        agreement_date = date.today()
    member = Entity()
    member.is_member = True
    member.name = name
    member.email = email
    member.phone = phone
    member.joined_date = joined_date
    member.agreement_date = agreement_date
    if is_keyholder is None:
        member.is_keyholder = False
    else:
        member.is_keyholder = is_keyholder

    member.save()

    return member.id


def update(member_id, name, email, phone, joined_date=None, agreement_date=None,
           is_keyholder=False):
    member = Entity.get((Entity.id == member_id) & Entity.is_member)
    member.name = name
    member.email = email
    member.phone = phone
    if joined_date is not None:
        member.joined_date = joined_date
    if agreement_date is not None:
        member.agreement_date = agreement_date
    if is_keyholder is None:
        member.is_keyholder = False
    else:
        member.is_keyholder = is_keyholder

    return member.save()


def create_token(email):
    member = Entity.get((Entity.email == email) & Entity.is_member)
    member.token = __generate_token()
    member.token_expiry = datetime.now() + timedelta(hours=24)
    member.save()
    return member.token


def authenticate_token(token):
    try:
        member = Entity.get(Entity.token == token)
        if (member.token_expiry > datetime.now()):
            return member
    except:
        pass
    return None  # no such token for member, or token is expired


def invalidate_token(id):
    member = Entity.get(Entity.id == id)
    member.token = None
    member.token_expiry = None
    member.save()


def __generate_token():
    alphabet = string.ascii_lowercase + string.digits
    size = 16

    # http://stackoverflow.com/a/2257449
    token = ''.join(random.choice(alphabet) for _ in range(size))
    return token
