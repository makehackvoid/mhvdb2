from mhvdb2 import app
from mhvdb2.models import Entity, Payment
from flask import render_template, request, flash
from peewee import DoesNotExist
from mhvdb2.resources import payments, members


def get_post_value(key):
    try:
        return request.form[key]
    except KeyError:
        return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup/', methods=['GET'])
def signup_get():
    return render_template('signup.html')


@app.route('/signup/', methods=['POST'])
def signup_post():
    name = get_post_value("name")
    email = get_post_value("email")
    phone = get_post_value("phone")

    errors = members.validate(name, email, phone)

    # Check if the "agree" checkbox was ticked
    if get_post_value("agree") is None:
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
    amount = get_post_value("amount")
    email = get_post_value("email")
    method = get_post_value("method")
    type = get_post_value("type")
    notes = get_post_value("notes")
    reference = get_post_value("reference")

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
    return render_template('admin.html')

@app.route('/admin/members')
def admin_members():
    members = Entity.select().where(Entity.is_member)
    return render_template('admin/members.html', members=members)

@app.route('/admin/transactions')
def admin_transactions():
    transactions = Payment.select()
    return render_template('admin/transactions.html', transactions=transactions)
