from flask import Flask, g
from peewee import *

app = Flask(__name__)
app.config.from_object('settings')
database = SqliteDatabase(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = database
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

from mhvdb2.models import Entity, Payment
import mhvdb2.views

database.connect()
if not Entity.table_exists(): Entity.create_table()
if not Payment.table_exists(): Payment.create_table()
database.close()
