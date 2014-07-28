from mhvdb2 import app, mailer
from flask import render_template, request, flash, redirect, url_for
from mhvdb2 import resources
from datetime import datetime


def get_post_value(key):
    try:
        return request.form[key]
    except KeyError:
        return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup/', methods=['GET'])
def signup():
    return render_template('signup.html')


@app.route('/signup/', methods=['POST'])
def signup_post():
    name = get_post_value("name")
    email = get_post_value("email")
    phone = get_post_value("phone")

    errors = resources.members.validate(name, email, phone)

    # Check if the "agree" checkbox was ticked
    if get_post_value("agree") is None:
        errors.append("You must agree to the rules and code of conduct to become a member!")

    if resources.members.exists(email):
        errors.append("There is already a member with that email address!")

    if len(errors) > 0:  # This means that an error has occured
        for e in errors:
            flash(e, 'danger')

        return render_template('signup.html', name=name, email=email,
                               phone=phone), 400

    resources.members.create(name, email, phone)

    flash("Thanks for registering!", "success")
    mailer.send(email, "Welcome to MakeHackVoid!",
                render_template("emails/signup.txt", name=name))
    return signup()


@app.route('/renew/', methods=['GET'])
def renew():
    return render_template("renew.html")


@app.route('/renew/', methods=['POST'])
def renew_post():
    email = get_post_value("email")

    if resources.members.exists(email):
        token = resources.members.create_token(email)
        url = url_for("renew_token", token=token, _external=True)
        mailer.send(email, "MakeHackVoid Membership Renewal",
                    render_template("emails/renew.txt", url=url))
        flash("Please the confirmation link sent to your email address to continue.", "info")
        return render_template("renew.html")
    else:
        flash("Sorry, no user exists with that email address.", "danger")
        return render_template("renew.html", email=email)


@app.route('/renew/<token>', methods=['GET'])
def renew_token(token):
    member = resources.members.authenticate_token(token)
    if member is None:
        flash("Invalid token", "danger")
        return redirect(url_for("renew"))
    return render_template("renew_token.html", name=member.name,
                           email=member.email, phone=member.phone)


@app.route('/renew/<token>', methods=['POST'])
def renew_token_post(token):
    member = resources.members.authenticate_token(token)
    name = get_post_value("name")
    email = get_post_value("email")
    phone = get_post_value("phone")
    if member is None:
        flash("Invalid token", "danger")
        return redirect(url_for("renew"))

    errors = resources.members.validate(name, email, phone)
    if len(errors) > 0:  # This means that an error has occured
        for e in errors:
            flash(e, 'danger')
        return render_template('renew_token.html', name=name, email=email, phone=phone), 400

    resources.members.update(member.id, name, email, phone, None, datetime.now())
    resources.members.invalidate_token(member.id)
    flash("Your resources.members.ip has been renewed.", "success")

    return redirect(url_for("index"))


@app.route('/payments/', methods=['GET'])
def payments():
    return render_template('payments.html')


@app.route('/payments/', methods=['POST'])
def payments_post():
    amount = get_post_value("amount")
    email = get_post_value("email")
    method = get_post_value("method")
    type = get_post_value("type")
    notes = get_post_value("notes")
    reference = get_post_value("reference")

    errors = resources.payments.validate(amount, email, method, type, notes, reference)

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

    resources.payments.create(amount, email, method, type, notes, reference)
    flash("Thank you!", "success")

    return payments()
