from mhvdb2 import app, database
from peewee import *


class BaseModel(Model):
    class Meta:
        database = database


class Entity(Model):
    """
    An Entity sends money to the organisation or recieves money from the
    organistaion. Members are a special type of entity.
    """
    name = CharField()
    email = CharField(null=True)  # Email is required for members
    is_member = BooleanField()  # Is the entity a member or past member


class Payment(Model):
    """
    A Payment is a transaction between an entity and the organisation. A
    payment can be either incoming or outgoing, depending on the sign of
    "amount".
    """
    time = DateTimeField()  # Date & time the payment occured
    entity = ForeignKeyField(Entity, related_name='payments')
    amount = IntegerField()  # Monetary amount in cents, e.g. $12.34 = 1234
    source = IntegerField(choice=[(0, 'Other'), (1, 'Bank Transfer')])
    is_donation = BooleanField()  # For members, donation vs payment for goods
    notes = TextField(null=True)
