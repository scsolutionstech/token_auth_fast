""" This file contains the Pydantic models for the API endpoints. """
from pydantic import BaseModel

class UserRegister(BaseModel):
    """ The UserRegister model.
    This model is used to validate the user registration data.
    """
    username: str
    password: str

class UserLogin(BaseModel):
    """ The UserLogin model.
    This model is used to validate the user login data.
    """
    username: str
    password: str

class TokenRefresh(BaseModel):
    """ The TokenRefresh model.
    This model is used to validate the token refresh data.
    """
    refresh_token: str

class SubscriptionCheck(BaseModel):
    """ The SubscriptionCheck model.
    This model is used to validate the subscription check data.
    """
    subscription_key: str

class SubscriptionDeactivate(BaseModel):
    """ The SubscriptionDeactivate model.
    This model is used to validate the subscription deactivation data.
    """
    subscription_key: str
