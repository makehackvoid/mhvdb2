from mhvdb2.models import Entity, Payment, User
from flask import render_template, request, flash, redirect, url_for
from .authentication import authenticate_user, register_user
from flask.ext.login import login_required, current_user, logout_user, current_app
from datetime import datetime
from . import admin
from mhvdb2 import resources


def get_post_value(key):
    try:
        return request.form[key]
    except KeyError:
        return None


@admin.route('/')
@login_required
def index():
    return render_template('admin/index.html')


@admin.route("/login", methods=["GET"])
def login():
    # If there are no users, send them to the registration page
    if User.select().count() == 0:
        flash("No admins found, please register the first administrator.", "info")
        return redirect(url_for(".register"))
    return render_template("admin/login.html")


@admin.route("/login", methods=["POST"])
def login_post():
    email = get_post_value("email")
    password = get_post_value("password")
    success = authenticate_user(email, password)
    if success:
        flash("Logged in successfully.", "success")
        next = request.args.get("next", '/')
        return redirect(next)
    else:
        flash("Incorrect email or password.", "danger")
        return render_template("admin/login.html", email=email)


@admin.route("/register", methods=["GET"])
def register():
    # Only allow access if logged in or no users are registered
    if current_user.is_anonymous() and User.select().count() > 0:
        return current_app.login_manager.unauthorized()

    return render_template("admin/register.html")


@admin.route("/register", methods=["POST"])
def register_post():
    # Only allow access if logged in or no users are registered
    if current_user.is_anonymous() and User.select().count() > 0:
        return current_app.login_manager.unauthorized()

    name = get_post_value("name")
    email = get_post_value("email")
    password = get_post_value("password")

    errors = register_user(name, email, password)
    if len(errors) > 0:  # This means that an error has occured
        for e in errors:
            flash(e, 'danger')
        return render_template("admin/register.html", name=name, email=email)
    else:
        flash("User registered successfully.", "success")
        return redirect(url_for('.register'))


@admin.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('.index'))


@admin.route('/members')
@login_required
def members():
    members = Entity.select().where(Entity.is_member)
    return render_template('admin/members.html', members=members)


@admin.route('/members/new', methods=['GET'])
@login_required
def member_new():
    return render_template('admin/member.html', new=True)


@admin.route('/members/new', methods=['POST'])
@login_required
def member_new_post():
    name = get_post_value("name")
    email = get_post_value("email")
    phone = get_post_value("phone")
    joined_date = get_post_value("joined_date")
    agreement_date = get_post_value("agreement_date")
    is_keyholder = get_post_value("is_keyholder")

    errors = resources.members.validate(name, email, phone, joined_date,
                                        agreement_date, is_keyholder)

    if resources.members.exists(email):
        errors.append("There is already a member with that email address!")

    if len(errors) > 0:  # This means that an error has occured
        for e in errors:
            flash(e, 'danger')
        return render_template('admin/member.html', name=name, email=email, phone=phone,
                               joined_date=joined_date, agreement_date=agreement_date,
                               is_keyholder=is_keyholder), 400

    joined_date = datetime.strptime(joined_date, '%Y-%m-%d').date()
    agreement_date = datetime.strptime(agreement_date, '%Y-%m-%d').date()

    resources.members.create(name, email, phone, joined_date, agreement_date, is_keyholder)
    flash("Member created", "success")

    return redirect(url_for('.members'))


@admin.route('/members/<int:id>', methods=['GET'])
@login_required
def member(id):
    member = resources.members.get(id)
    if member:
        return render_template('admin/member.html', name=member.name, email=member.email,
                               phone=member.phone, joined_date=member.joined_date,
                               agreement_date=member.agreement_date,
                               is_keyholder=member.is_keyholder)
    else:
        return redirect(url_for('.members'))


@admin.route('/members/<int:id>', methods=['POST'])
@login_required
def member_post(id):
    name = get_post_value("name")
    email = get_post_value("email")
    phone = get_post_value("phone")
    joined_date = get_post_value("joined_date")
    agreement_date = get_post_value("agreement_date")
    is_keyholder = get_post_value("is_keyholder")

    errors = resources.members.validate(name, email, phone, joined_date,
                                        agreement_date, is_keyholder)

    if resources.members.exists(email, id):
        errors.append("There is already a member with that email address!")

    if len(errors) > 0:  # This means that an error has occured
        for e in errors:
            flash(e, 'danger')
        return render_template('admin/member.html', id=id, name=name, email=email,
                               phone=phone, joined_date=joined_date,
                               agreement_date=agreement_date,
                               is_keyholder=is_keyholder), 400

    joined_date = datetime.strptime(joined_date, '%Y-%m-%d').date()
    agreement_date = datetime.strptime(agreement_date, '%Y-%m-%d').date()

    resources.members.update(id, name, email, phone, joined_date, agreement_date, is_keyholder)

    flash("Member updated", "success")

    return redirect(url_for('.members'))


@admin.route('/transactions')
@login_required
def transactions():
    transactions = Payment.select()
    return render_template('admin/transactions.html', transactions=transactions)


@admin.route('/entities')
@login_required
def entities():
    entities = Entity.select().where(Entity.is_member == False)          # noqa
    return render_template('admin/entities.html', entities=entities)


@admin.route('/entities/new', methods=['GET'])
@login_required
def entity_new():
    return render_template('admin/entity.html', new=True)


@admin.route('/entities/new', methods=['POST'])
@login_required
def entity_new_post():
    name = get_post_value("name")
    email = get_post_value("email")
    phone = get_post_value("phone")

    errors = resources.entities.validate(name, email, phone)

    if len(errors) > 0:  # This means that an error has occured
        for e in errors:
            flash(e, 'danger')
        return render_template('admin/entity.html', new=True, name=name, email=email,
                               phone=phone), 400

    id = resources.entities.create(name, email, phone)
    flash("Entity created", "success")

    return redirect(url_for('.entity', id=id))


@admin.route('/entities/<int:id>', methods=['GET'])
def entity(id):
    entity = resources.entities.get(id)
    if entity:
        return render_template('admin/entity.html', name=entity.name, email=entity.email,
                               phone=entity.phone)
    else:
        return redirect(url_for('.entities'))


@admin.route('/entities/<int:id>', methods=['POST'])
@login_required
def entity_post(id):
    name = get_post_value("name")
    email = get_post_value("email")
    phone = get_post_value("phone")

    errors = resources.entities.validate(name, email, phone)

    if len(errors) > 0:  # This means that an error has occured
        for e in errors:
            flash(e, 'danger')
        return render_template('admin/entity.html', id=id, name=name, email=email,
                               phone=phone), 400

    resources.entities.update(id, name, email, phone)
    flash("Entity updated", "success")

    return redirect(url_for('.entities'))
