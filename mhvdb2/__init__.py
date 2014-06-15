from flask import Flask, g
from peewee import *   # noqa

app = Flask(__name__)
app.config.from_object('settings')
database = SqliteDatabase(app.config['DATABASE'], threadlocals=True)


@app.before_request
def before_request():
    g.db = database
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response

import mhvdb2.routes   # noqa

from mhvdb2.models import Entity, Payment

database.connect()
if not Entity.table_exists():
    Entity.create_table()
if not Payment.table_exists():
    Payment.create_table()
database.close()
