from mhvdb2 import app, database
from peewee import *

class BaseModel(Model):
    class Meta:
        database = database
