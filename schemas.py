from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# Schema for user registration and output
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True  # Updated from orm_mode to from_attributes


# Token schema for responses
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


# Additional schema for token output including metadata
class TokenOut(BaseModel):
    access_token: str
    token_type: str


class SubscriptionBase(BaseModel):
    key: str
    created_date: datetime
    end_date: datetime
    last_checkout: datetime
    is_active: bool

    class Config:
        orm_mode = True
        from_attributes = True

class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None