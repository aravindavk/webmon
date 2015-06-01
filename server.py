#!/usr/bin/python

# server.py
# :copyright: (c) 2015 by Aravinda VK <mail@aravindavk.in>
# :license: MIT, see LICENSE for more details.

from flask import Flask, render_template, request
from users import Users
from urlparse import urlparse
from config import APP_DEBUG

import timeline

app = Flask(__name__)
app.debug = APP_DEBUG


@app.route("/v1/user/pins/<pinid>", methods=["PUT"])
def user_pins(pinid):
    """
    PUT /v1/user/pins/<pinid>
    Only for Testing, prints sent data in Console
    When API_ROOT = "http://localhost:5000"
    """
    print request.get_data()
    print request.headers
    return "Pin sent successfully"


@app.route('/')
def hello_world():
    """
    GET /
    Home page
    """
    return 'Hello World!'


@app.route("/save", methods=["POST"])
def save():
    """
    POST /save
    """
    user_token = request.form["user_token"]
    enabled = request.form["enabled"]
    parsed_uri = urlparse(request.form["url"])

    # Parse the URL, if lengthy URL get only domain name
    if parsed_uri.path:
        domain = parsed_uri.path
    else:
        domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)

    # Enabled flag to save in db
    enabled = 1 if enabled == "true" else 0

    webmon_users = Users()
    users = webmon_users.get(user_token)
    if users.count() > 0:
        # If user already exists
        user = users.first()
        # If no changes compared to previous change
        if user.url == domain and user.enabled == enabled:
            return "URL added successfully"

        # Update to Db and send notification
        webmon_users.update(user, user_token, domain, enabled)
        timeline.send_update_notification(user_token, domain,
                                          enabled, update=True)
    else:
        # New Registration, add to db and send notification
        webmon_users.add(user_token, domain, enabled)
        timeline.send_update_notification(user_token, domain,
                                          enabled, update=False)
    return "URL added successfully"


@app.route("/settings")
def settings():
    """
    Settings page when App config is opened.
    """
    return render_template("settings.html")


if __name__ == "__main__":
    """
    For testing run,
        python server.py
    App starts by default in port 5000
    """
    app.run(threaded=True)
