from mhvdb2 import app
from mhvdb2.models import Entity
from flask import render_template, request, flash
import re
from datetime import date
from peewee import DoesNotExist
import json

from mhvdb2.resources import *


# Response object (must be returned by resource call, is a dictionary)
#
# "data"     -> dictionary to pass to html renderer, or turned into JSON
# "status"   -> HTTP status code
# "flash"    -> (message, code) tuple to be handed to flash(message, code)
# "redirect" -> url to redirect to (302)
#
# web() takes two parameters:
#   response  -> the response object from the resource
#   template  -> name of the html template to render (default: "index.html")
#   kind      -> either "json" or "html" (default: "html")
def web(response, template="index.html", kind="html"):
    if "status" in response:
        status = response["status"]
    else:
        status = 200

    if kind == "html":
        if "flash" in response:
            flash(response["flash"][0], response["flash"][1])

        return (render_template(template, data=response["data"]), status, {})
    
    # otherwise JSON
    else:
        return (json.dumps(response["data"]), status, {"Content-Type": "text/json"})


@app.route('/')
def index():
    return web(Application.show(request))

@app.route('/.json')
def index_json():
    return web(Application.show(request), kind="json")

@app.route('/signup/', methods=['GET'])
def signup_get():
    return render_template('signup.html')


@app.route('/signup/', methods=['POST'])
def signup_post():
    return web(User.create(request), template = 'signup.html')

