from flask import Flask
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

import mhvdb2.models
import mhvdb2.views
