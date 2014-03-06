from mhvdb2 import app, database
from peewee import *


class BaseModel(Model):
    class Meta:
        database = database


class Entity(Model):
    name = CharField()
    email = CharField()
    is_member = BooleanField()


class Payment(Model):
    time = DateTimeField()
    entity = ForeignKeyField(Entity, related_name='payments')
    amount = IntegerField()
    source = IntegerField()
    is_donation = BooleanField()
    notes = TextField()
