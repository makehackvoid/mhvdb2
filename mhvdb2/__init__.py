from flask import Flask, g
from peewee import *   # noqa

app = Flask(__name__)
app.config.from_object('settings')
database = SqliteDatabase(app.config['DATABASE'], threadlocals=True)


from mhvdb2.authentication import login_manager
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "danger"


@app.before_request
def before_request():
    g.db = database
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response

import mhvdb2.routes   # noqa

from mhvdb2.models import Entity, Payment, User

database.connect()
if not Entity.table_exists():
    Entity.create_table()
if not Payment.table_exists():
    Payment.create_table()
if not User.table_exists():
    User.create_table()
database.close()
