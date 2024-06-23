""" This file contains the database models for the application. """

from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """The User model.
    This model is used to store the user information in the database.

    Attributes:
        id: int: The user's id.
        username: str: The user's username.
        email: str: The user's email.
        password: str: The user's password.
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)


class Subscription(Base):
    """The Subscription model.
    This model is used to store the subscription information in the database.

    Attributes:
        id: int: The subscription's id.
        key: str: The subscription's key.
        is_active: bool: The subscription's status.
        create_date: datetime: The subscription's creation date.
        start_date: datetime: The subscription's start date.
        end_date: datetime: The subscription's end date.
    """
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    create_date = Column(DateTime, default=datetime.utcnow)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, default=datetime.utcnow() + timedelta(days=365))
