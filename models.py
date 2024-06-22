# models.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime,timedelta

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    create_date = Column(DateTime, default=datetime.utcnow)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, default=datetime.utcnow() + timedelta(days=365))


