from mhvdb2 import app
from mhvdb2.models import Entity
from flask import render_template, request, flash
import re
from datetime import date
from peewee import DoesNotExist


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup/', methods=['GET'])
def signup_get():
    return render_template('signup.html')


@app.route('/signup/', methods=['POST'])
def signup_post():
    # Get inputs from form
    first_name = request.form["first-name"].strip()
    last_name = request.form["last-name"].strip()
    email = request.form["email"].strip()
    phone = request.form["phone"].strip()

    # Validate inputs
    valid = True
    if not first_name or not last_name:
        flash("Sorry, you need to provide a name.", 'danger')
        valid = False
    if not phone:
        flash("Sorry, you need to provide a phone number.", 'danger')
        valid = False
    if not re.match("[^@\s]+@[^@\s]+", email):
        flash("Sorry, you need to provide an email address.", 'danger')
        valid = False

    if not valid:
        return render_template('signup.html', first_name=first_name,
                               last_name=last_name, email=email)

    # Create / Update member
    member = None
    try:
        member = Entity.get(Entity.email == email)
        flash("Thanks for renewing, your details have been updated!",
              "success")
    except DoesNotExist:
        member = Entity()
        member.is_member = True
        member.joined_date = date.today()
        flash("Thanks for registering!", "success")

    member.name = first_name + ' ' + last_name
    member.email = email
    member.phone = phone
    member.agreement_date = date.today()
    member.save()

    return signup_get()


@app.route('/admin/')
def admin():
    members = Entity.select().where(Entity.is_member)
    return render_template('admin.html', members=members)
