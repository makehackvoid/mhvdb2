from mhvdb2 import app
import os
from datetime import datetime
import requests


def send(to, subject, body):
    if app.debug:
        mock_send(to, subject, body)
    else:
        mailgun_send(to, subject, body)


def mailgun_send(to, subject, body):
    endpoint = "https://api.mailgun.net/v2/{}/messages".format(app.config["MAILGUN_DOMAIN"])
    auth = ("api", app.config["MAILGUN_API_KEY"])
    data = {"from": app.config["MAILGUN_FROM_ADDR"],
            "to": to,
            "subject": subject,
            "text": body}

    requests.post(endpoint, auth=auth, data=data, verify='/usr/lib/ssl/certs/bundle.CA_BUNDLE')


def mock_send(to, subject, body):
    # Calculate path to save mock email. Format: YY-MM-DD-SSSSS.txt
    now = datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    file = "{0:%y-%m-%d}-{1:07d}-{2}.txt".format(now, (now - midnight).microseconds, to)
    folder = "mock_emails"
    path = os.path.join(folder, file)

    # Make sure folder exists
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Write mock email to file
    f = open(path, 'w+')
    f.write("To: " + to + "\n")
    f.write("Subject: " + subject + "\n\n")
    f.write(body)
