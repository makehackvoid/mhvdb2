from mhvdb2 import app
from mhvdb2.models import Entity
from flask import render_template, request, flash
from peewee import DoesNotExist
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

    errors = members.validate(name, email, phone)

    # Check if the "agree" checkbox was ticked
    try:
        agree = request.form["agree"]
    except KeyError:
        errors.append("You must agree to the terms and conditions!")

    if len(errors) > 0:  # This means that an error has occured
        for e in errors:
            flash(e, 'danger')

        return render_template('signup.html', name=name, email=email,
                               phone=phone), 400

    try:
        members.update(name, email, phone)
        flash("Thanks for renewing, your details have been updated!",
              "success")
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

    errors = payments.validate(amount, email, method, type, notes, reference)

    if len(errors) > 0:  # this means that an error has occured
        for e in errors:
            flash(e, 'danger')
        return render_template('payments.html', amount=amount, email=email,
                               method=method, type=type, notes=notes,
                               reference=reference), 400

    # Cajole the post data into integers
    amount = int(amount)
    type = int(type)
    method = int(method)

    payments.create(amount, email, method, type, notes, reference)
    flash("Thank you!", "success")

    return payments_get()


@app.route('/admin/')
def admin():
    members = Entity.select().where(Entity.is_member)
    return render_template('admin.html', members=members)
