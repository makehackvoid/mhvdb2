from mhvdb2 import app
from mhvdb2.models import Entity, Payment
from flask import render_template, request, flash
import re
from datetime import date, datetime
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
    name = request.form["name"].strip()
    email = request.form["email"].strip()
    phone = request.form["phone"].strip()

    # Validate inputs
    valid = True
    if not name:
        flash("Sorry, you need to provide a name.", 'danger')
        valid = False
    if not phone:
        flash("Sorry, you need to provide a phone number.", 'danger')
        valid = False
    if not re.match("[^@\s]+@[^@\s]+", email):
        flash("Sorry, you need to provide an email address.", 'danger')
        valid = False

    if not valid:
        return render_template('signup.html', name=name, email=email)

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

    member.name = name
    member.email = email
    member.phone = phone
    member.agreement_date = date.today()
    member.save()

    return signup_get()


@app.route('/payments/', methods=['GET'])
def payments_get():
    return render_template('payments.html')


@app.route('/payments/', methods=['POST'])
def payments_post():
    # Get inputs from form
    amount = request.form["amount"].strip()
    email = request.form["email"].strip()
    method = request.form["method"].strip()
    type = request.form["type"].strip()
    notes = request.form["notes"].strip()
    reference = request.form["reference"].strip()


    # Validate inputs
    valid = True

    if not amount or not amount.isdigit() or int(amount) <=0:
        flash("Sorry, you need to provide a valid amount.", 'danger')
        valid = False
    if not re.match("[^@\s]+@[^@\s]+", email):
        flash("Sorry, you need to provide a valid email address.", 'danger')
        valid = False
    if not type or not type.isdigit() or int(type) > 2:
        flash("Sorry, you need to provide a valid payment type.", 'danger')
        valid = False
    if not method or not method.isdigit() or int(method) > 2:
        flash("Sorry, you need to provide a valid payment method.", 'danger')
        valid = False
    if not reference:
        flash("Sorry, you need to provide a reference.", 'danger')
        valid = False

    entity = None
    try: 
        Entity.get(Entity.email == email)
    except DoesNotExist: 
        flash("Sorry, you need to provide a valid member's email address.", 'danger')
        valid = False

    if not valid:
        return render_template('payments.html', amount=amount, email=email,
            method=method, type=type, notes=notes, reference=reference)

    # Cajole the post data into integers
    amount = int(amount)
    type = int(type)
    method = int(method)

    # Create payment
    payment = Payment()
    payment.time = datetime.now()
    payment.entity = Entity.get(Entity.email == email)
    payment.amount = amount
    payment.source = method
    payment.is_donation = type != 0
    payment.notes = notes
    if method == 0: # Bank transfer
        payment.bank_reference = reference
    payment.pending = True
    payment.save()

    flash("Thank you!", "success")

    return payments_get()


@app.route('/admin/')
def admin():
    members = Entity.select().where(Entity.is_member)
    return render_template('admin.html', members=members)
