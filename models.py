from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    subscription_key = Column(String, unique=True, index=True)
    creation_date = Column(DateTime, default=datetime.utcnow)
    expiry_date = Column(DateTime)
    last_checked = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
