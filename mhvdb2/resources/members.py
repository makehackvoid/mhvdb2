from mhvdb2 import app
from mhvdb2.models import Entity, Payment
from flask import render_template, request, flash
import re
from datetime import date, datetime
from peewee import DoesNotExist


def validate(name, email, phone):
    errors = []
    if not name:
        errors.append("Sorry, you need to provide a name.")
    if not phone:
        errors.append("Sorry, you need to provide a phone number.")
    if not re.match("[^@\s]+@[^@\s]+", email):
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
    if(member == None): 
        member = Entity.get(Entity.email == email)
    member.name = name
    member.email = email
    member.phone = phone
    member.agreement_date = date.today()

    return member.save()

