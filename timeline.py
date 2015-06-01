#!/usr/bin/python

# timeline.py
# :copyright: (c) 2015 by Aravinda VK <mail@aravindavk.in>
# :license: MIT, see LICENSE for more details.

from datetime import datetime
import requests
import json
import time

from config import API_ROOT


def _send_pin(user_token, pin):
    """
    Generic function to send Pin, Pushes PIN to Timeline server
    as HTTP PUT request, adds required header and stringifies the
    pin object.
    """
    url = "%s/v1/user/pins/%s" % (API_ROOT, pin["id"])
    resp = requests.put(url, headers={"X-User-Token": user_token,
                                      "Content-Type": "application/json"},
                        data=json.dumps(pin))

    if resp.status_code < 300:
        return resp.content
    elif resp.status_code == 400:
        return "The pin object submitted was invalid."
    elif resp.status_code == 403:
        return "The API key submitted was invalid."
    elif resp.status_code == 410:
        return "The user token submitted was invalid or does not exist."
    elif resp.status_code == 429:
        return "Server is sending updates too quickly."
    elif resp.status_code == 503:
        return "Could not save pin due to a temporary server error."
    else:
        return "Unknown error. Status code: %s" % resp.status_code


def send_notification(user_token, title, subtitle, warning=False):
    """
    When some state changes, this func is triggered.
    Prepares the PIN object with proper messages
    """
    now = datetime.utcnow().isoformat() + 'Z'
    tinyIcon = "system://images/NOTIFICATION_FLAG"
    if warning:
        tinyIcon = "system://images/GENERIC_WARNING"

    pin = {
        "id": "webmon-message-%s" % time.time(),
        "time": now,
        "layout": {
            "type": "genericPin",
            "tinyIcon": tinyIcon,
            "title": title,
            "subtitle": subtitle
        },
        "createNotification": {
            "layout": {
                "type": "genericPin",
                "tinyIcon": tinyIcon,
                "title": title,
                "subtitle": subtitle
            }
        }
    }
    return _send_pin(user_token, pin)


def send_update_notification(user_token, url, enabled=1, update=False):
    """
    When user subscribed for first time or when config is updated
    Prepares the PIN object with proper messages and calls _send_pin
    """
    now = datetime.utcnow().isoformat() + 'Z'
    tinyIcon = "system://images/NOTIFICATION_FLAG"
    title = "Hello from Webmon"
    subtitle = "Registered your website address %s. " % url

    if update:
        title = "Message from Webmon"
        subtitle = "Website address updated to %s. " % url

    if enabled == 1:
        subtitle += "Tracking is enabled"
    else:
        subtitle += "Tracking is disabled"

    pin = {
        "id": "webmon-message-%s" % time.time(),
        "time": now,
        "layout": {
            "type": "genericPin",
            "tinyIcon": tinyIcon,
            "title": title,
            "subtitle": subtitle
        },
        "createNotification": {
            "layout": {
                "type": "genericPin",
                "tinyIcon": tinyIcon,
                "title": title,
                "subtitle": subtitle
            }
        }
    }
    return _send_pin(user_token, pin)
