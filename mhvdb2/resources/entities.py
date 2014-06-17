from mhvdb2.models import Entity
from peewee import DoesNotExist
import re


def get(entity_id):
    try:
        return Entity.get(Entity.id == entity_id)
    except DoesNotExist:
        return None


def validate(name, email, phone):
    errors = []
    if not name:
        errors.append("Sorry, you need to provide a name.")
    if email and not re.match("[^@\s]+@[^@\s]+", email):
        errors.append("Sorry, that isn't a valid email address.")

    return errors


def create(name, email, phone):
    entity = Entity()
    entity.is_member = False
    entity.name = name
    entity.email = email
    entity.phone = phone
    entity.save()
    return entity.id


# Update entity
def update(entity_id, name, email, phone):
    entity = Entity.get(Entity.id == entity_id)
    entity.name = name
    entity.email = email
    entity.phone = phone
    entity.save()
