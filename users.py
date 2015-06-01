#!/usr/bin/python

# users.py
# :copyright: (c) 2015 by Aravinda VK <mail@aravindavk.in>
# :license: MIT, see LICENSE for more details.

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine, DateTime
from sqlalchemy import UniqueConstraint, distinct, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from config import DB_USER, DB_PASSWD, DB_HOST, DB_PORT, DB_NAME

DB_URL = "postgresql://{}:{}@{}:{}/{}".format(DB_USER,
                                              DB_PASSWD,
                                              DB_HOST,
                                              DB_PORT,
                                              DB_NAME
                                              )
Base = declarative_base()


class User(Base):
    """
    User table initialization.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    token = Column(String)
    url = Column(String)
    state = Column(Integer)
    enabled = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=datetime.now)
    __table_args__ = (UniqueConstraint('token', 'url'), )


class Users(object):
    """
    Users object, provides utility function to interact with
    users table in DB
    """
    def __init__(self):
        """
        Create connection and session, Try creating table,
        required only for first time
        """
        engine = create_engine(DB_URL)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)

    def get(self, user_token):
        """
        Gets a User, based on input user_token
        """
        return self.session.query(User).filter(User.token == user_token)

    def add(self, user_token, url, enabled):
        """
        Add user to users table
        """
        user = User(token=user_token, url=url, enabled=enabled)
        try:
            self.session.add(user)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()

    def update(self, user, user_token, url, enabled):
        """
        Update users detail in users table
        """
        user.url = url
        user.enabled = enabled
        self.session.commit()

    def update_state(self, url, state):
        """
        Update the Website state
        """
        query = self.session.query(User).filter(User.url == url)
        query.update({"state": state})
        self.session.commit()

    def get_distinct_urls(self):
        """
        Queries and gets distinct enabled URLS from users table
        """
        return self.session.query(distinct(User.url),
                                  User.state).filter(User.enabled == 1)

    def get_users_from_url(self, url):
        """
        Get all enabled subscribed users for a url.
        """
        return self.session.query(User).filter(User.url == url,
                                               User.enabled == 1)
