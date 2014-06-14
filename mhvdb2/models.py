from mhvdb2 import database
from peewee import *


class BaseModel(Model):
    class Meta:
        database = database


class Entity(BaseModel):
    """
    An Entity sends money to the organisation or recieves money from the
    organistaion. Members are a special type of entity.
    """
    is_member = BooleanField()  # Is the entity a member (past or present)
    name = CharField()
    email = CharField(null=True)  # Email is required for members
    phone = CharField(null=True)
    reminder_date = DateField(null=True)  # When to send reminder to member
    joined_date = DateField(null=True)  # date the person first joined
    agreement_date = DateField(null=True)  # date the person agreed to rules


class Payment(BaseModel):
    """
    A Payment is a transaction between an entity and the organisation. A
    payment can be either incoming or outgoing, depending on the sign of
    "amount".
    """
    time = DateTimeField()  # Date & time the payment occured
    entity = ForeignKeyField(Entity, related_name='payments')
    amount = IntegerField()  # Monetary amount in cents, e.g. $12.34 = 1234
    source = IntegerField(choices=[(0, 'Other'), (1, 'Bank Transfer')])
    is_donation = BooleanField()  # For members, donation vs payment for goods
    notes = TextField(null=True)
    bank_reference = CharField(null=True)  # For bank transfers
    pending = BooleanField()
