from mhvdb2 import app
from mhvdb2.models import Entity
from flask import render_template, request, flash
import re
from datetime import date
from peewee import DoesNotExist
import json
from mhvdb2.resources import payments, members


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup/', methods=['GET'])
def signup_get():
    return render_template('signup.html')

@app.route('/signup/', methods=['POST'])
def signup_post():
    name = request.form["name"].strip()
    email = request.form["email"].strip()
    phone = request.form["phone"].strip()

    flashes = members.validate(name, email, phone)

    if len(flashes) > 0: #this means that an error has occured
        for f in flashes:
            flash(f, 'danger')

        return render_template('signup.html'), 400

    try:
        member = Entity.get(Entity.email == email)
        members.update(member, name, email, phone)
        flash("Thanks for renewing, your details have been updated!", "success")
    except DoesNotExist:
        members.create(name, email, phone)
        flash("Thanks for registering!", "success")

    return signup_get()

@app.route('/payments/', methods=['GET'])
def payments_get():
    return render_template('payments.html')

@app.route('/payments/', methods=['POST'])
def payments_post():
    amount = request.form["amount"].strip()
    email = request.form["email"].strip()
    method = request.form["method"].strip()
    type = request.form["type"].strip()
    notes = request.form["notes"].strip()
    reference = request.form["reference"].strip()

    flashes = payments.validate(amount, email, method, type, notes, reference)

    entity = None
    try: 
        entity = Entity.get(Entity.email == email)
    except DoesNotExist: 
        flashes.append("Sorry, you need to provide a valid member's email address.")

    if len(flashes) > 0: #this means that an error has occured
        for f in flashes:
            flash(f, 'danger')
        return render_template('payments.html', amount=amount, email=email,
            method=method, type=type, notes=notes, reference=reference), 400
    
    # Cajole the post data into integers
    amount = int(amount)
    type = int(type)
    method = int(method)

    payments.create(amount, entity, method, type, notes, reference)
    flash("Thank you!", "success")

    return payments_get()

@app.route('/admin/')
def admin():
    members = Entity.select().where(Entity.is_member)
    return render_template('admin.html', members=members)

