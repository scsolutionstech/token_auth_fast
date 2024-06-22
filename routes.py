from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from controller import register_user, authenticate_user, create_tokens, refresh_access_token, check_subscription, deactivate_subscription
from database import get_db
from utils import get_current_user
from models import User

auth_router = APIRouter()
subscription_router = APIRouter()

class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class TokenRefresh(BaseModel):
    refresh_token: str

class SubscriptionCheck(BaseModel):
    subscription_key: str

class SubscriptionDeactivate(BaseModel):
    subscription_key: str

@auth_router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    db_user = register_user(db, user.username, user.password)
    return {"username": db_user.username}

@auth_router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.username, user.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    tokens = create_tokens(db_user.id)
    return tokens

@auth_router.post("/refresh")
def refresh(token: TokenRefresh):
    new_tokens = refresh_access_token(token.refresh_token)
    return new_tokens

@subscription_router.post("/check")
def check(subscription: SubscriptionCheck, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = check_subscription(db, subscription.subscription_key)
    return result

@subscription_router.post("/deactivate")
def deactivate(subscription: SubscriptionDeactivate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    deactivate_subscription(db, subscription.subscription_key)
    return {"message": "Subscription deactivated"}
