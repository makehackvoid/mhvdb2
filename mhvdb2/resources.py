from mhvdb2 import app
from mhvdb2.models import Entity
from flask import render_template, request, flash
import re
from datetime import date
from peewee import DoesNotExist

class Resource:
    pass

class User(Resource):
    def show(data):
        pass

    @staticmethod
    def create(data):
        res = {"data": None}

        # Get inputs from form
        first_name = data.form["first-name"].strip()
        last_name = data.form["last-name"].strip()
        email = data.form["email"].strip()
        phone = data.form["phone"].strip()

        # Validate inputs
        valid = True
        if not first_name or not last_name:
            res["flash"] = ("Sorry, you need to provide a name.", 'danger')
            valid = False
        if not phone:
            res["flash"] = ("Sorry, you need to provide a phone number.", 'danger')
            valid = False
        if not re.match("[^@\s]+@[^@\s]+", email):
            res["flash"] = ("Sorry, you need to provide an email address.", 'danger')
            valid = False

        if not valid:
            res["status"] = 400
            res["data"] = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email }
            return res

        # Create / Update member
        member = None
        try:
            member = Entity.get(Entity.email == email)
            res["flash"] = ("Thanks for renewing, your details have been updated!",
                  "success")
        except DoesNotExist:
            member = Entity()
            member.is_member = True
            member.joined_date = date.today()
            res["flash"] = ("Thanks for registering!", "success")

        member.name = first_name + ' ' + last_name
        member.email = email
        member.phone = phone
        member.agreement_date = date.today()
        member.save()

        res["status"] = 200
        return res


class Application(Resource):
    @staticmethod
    def show(data):
        return {"data":None}

