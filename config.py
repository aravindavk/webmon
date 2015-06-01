#!/usr/bin/python

# config.py
# :copyright: (c) 2015 by Aravinda VK <mail@aravindavk.in>
# :license: MIT, see LICENSE for more details.

import os


APP_DEBUG = False
DB_HOST = os.getenv("OPENSHIFT_POSTGRESQL_DB_HOST", "localhost")
DB_PORT = os.getenv("OPENSHIFT_POSTGRESQL_DB_PORT", "5432")
DB_USER = "<DB_USER>"
DB_PASSWD = "<DB_PASSWD>"
DB_NAME = "<DB_NAME>"
API_ROOT = "https://timeline-api.getpebble.com"
