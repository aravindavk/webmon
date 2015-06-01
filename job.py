#!/usr/bin/python

# job.py
# :copyright: (c) 2015 by Aravinda VK <mail@aravindavk.in>
# :license: MIT, see LICENSE for more details.

import requests
from datetime import datetime

from users import Users
import timeline


def main():
    webmon = Users()
    state_changes = []

    for row in webmon.get_distinct_urls():
        # For each distinct URLs do HTTP GET request
        # and collect the status code
        try:
            resp = requests.get(row[0])
            status_code = resp.status_code
        except requests.exceptions.ConnectionError:
            status_code = -1

        # State Changed: If current state is not
        # equal to previous state, collect as state_changes
        if status_code != row[1]:
            state_changes.append((row[0], row[1], status_code))

    for url, old_state, new_state in state_changes:
        # For each state changes, send notification to all the
        # users who subscribed to that URL and enabled.
        if new_state == 200:
            # Good status, Website is Healty
            title = "Status: Healthy"
            subtitle = "%s is Up" % (url)
            warning = False
        else:
            # Bad status, may be temporary add error message along
            # with the actual message
            title = "Status: Faulty"
            subtitle = "%s is Down, Error code: %s" % (url, new_state)
            warning = True

        for user in webmon.get_users_from_url(url):
            # If multiple users subscribed to same URL
            # Send notification to all enabled users.
            resp = timeline.send_notification(user.token, title,
                                              subtitle, warning)
            print "[%s] URL: %s, Status: %s => %s, %s" % (datetime.utcnow(),
                                                          url,
                                                          old_state,
                                                          new_state,
                                                          resp)

        # Update the current status in db
        webmon.update_state(url, new_state)


if __name__ == "__main__":
    main()
