from mhvdb2 import database
from peewee import *   # noqa
from dateutil.relativedelta import relativedelta
from datetime import datetime


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    """
    A User is someone who has special access to the system that requires
    a login (only administrators, in this case)
    """
    name = CharField()
    email = CharField()
    password = CharField()


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
    is_keyholder = BooleanField(null=True)  # Does the member have a key?
    token = CharField(null=True)             # to authenticate members via email
    token_expiry = DateTimeField(null=True)  # expiry for the token

    def active_member(self):
        one_year_ago = (datetime.now() - relativedelta(years=1)).date()
        if self.agreement_date <= one_year_ago:
            return False
        else:
            return True
