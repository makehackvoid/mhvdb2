from mhvdb2.models import Entity, User
from flask import render_template, request, flash, redirect, url_for
from .authentication import authenticate_user, register_user
from flask.ext.login import login_required, current_user, logout_user, current_app
from datetime import datetime, date
from . import admin
from mhvdb2 import resources, app, mailer


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


@admin.route('/members/once_only_email', methods=['GET'])
@login_required
def member_once_only_email():
    '''
    Finds all expired members and sends once only email asking them to renew.
    Used for first run, before we setup regular emails as people expire.
    '''
    members = Entity.select().where(Entity.is_member)
    do_not_email = app.config['DO_NOT_EMAIL']
    # flash('do_not_email= ' + ', '.join(do_not_email))
    emails_sent = 0
    for member in members:
        if member.active_member():
            None
        else:
            if member.name in do_not_email:
                flash("Not emailing: " + member.name)
            else:
                if member.reminder_date:
                    flash("Not emailing: " + member.name + " reminder_date set "
                          + member.reminder_date.strftime('%m/%d/%Y'))
                else:
                    # only send this email to people who have not joined under new system (2014)
                    if member.agreement_date.year < 2014:
                        mailer.send(member.email,
                                    "MakeHackVoid Membership Renewal - once only reminder email",
                                    render_template("emails/once_only_renewal.txt",
                                                    name=member.name, email=member.email))
                        # set the reminder date in database so can test when sending another email
                        member.reminder_date = date.today()
                        member.save()
                        emails_sent += 1
    flash("Sent " + str(emails_sent) + " once only emails.")
    return redirect(url_for('.index'))


@admin.route('/members/renwal_email', methods=['GET'])
@login_required
def member_renewal_email():
    '''
    Finds all expired members who have been 'new style' members -
    that is they have agreement_date from 2014 onwards, and
    have not yet been sent a reminder
     - reminders_date tests will probably want to be a bit more complex
       at some stage
    Sends reminder email asking them to renew.
    '''
    members = Entity.select().where(Entity.is_member)
    do_not_email = app.config['DO_NOT_EMAIL']
    # flash('do_not_email= ' + ', '.join(do_not_email))
    emails_sent = 0
    for member in members:
        if member.active_member():
            None
        else:
            if member.name not in do_not_email:
                if member.agreement_date.year >= 2014 and not member.reminder_date:
                    mailer.send(member.email,
                                "MakeHackVoid membership renewal reminder",
                                render_template("emails/renewal_reminder.txt",
                                                name=member.name,
                                                email=member.email,
                                                agreement_date=member.agreement_date))
                    # set the reminder date in database so can test when sending another email
                    member.reminder_date = date.today()
                    member.save()
                    emails_sent += 1
    flash("Sent " + str(emails_sent) + " once only emails.")
    return redirect(url_for('.index'))


# I think we should remove entities that are not members as well?
@admin.route('/entities')
@login_required
def entities():
    entities = Entity.select().where(Entity.is_member == False)          # noqa
    return render_template('admin/entities.html', entities=entities)


# I think we should remove entities that are not members as well?
@admin.route('/entities/new', methods=['GET'])
@login_required
def entity_new():
    return render_template('admin/entity.html', new=True)


# I think we should remove entities that are not members as well?
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


# I think we should remove entities that are not members as well?
@admin.route('/entities/<int:id>', methods=['GET'])
def entity(id):
    entity = resources.entities.get(id)
    if entity:
        return render_template('admin/entity.html', name=entity.name, email=entity.email,
                               phone=entity.phone)
    else:
        return redirect(url_for('.entities'))


# I think we should remove entities that are not members as well?
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
