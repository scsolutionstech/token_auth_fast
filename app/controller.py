""" This module contains the functions that handle the business logic of the application. """

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from models import User, Subscription
from utils import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    JWT_SECRET_KEY,
    ALGORITHM,
)
from jose import jwt


def register_user(db: Session, username: str, password: str):
    """Register a new user."""
    user = db.query(User).filter(User.username == username).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists",
        )
    hashed_password = get_password_hash(password)
    db_user = User(username=username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        return False
    if not verify_password(password, db_user.hashed_password):
        return False
    return db_user


def create_tokens(user_id: int) -> dict[str, str]:
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user_id)}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": str(user_id)})
    return {"access_token": access_token, "refresh_token": refresh_token}


def refresh_access_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": user_id}, expires_delta=access_token_expires
        )
        return {"access_token": access_token}
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def check_subscription(db: Session, subscription_key: str):
    subscription = (
        db.query(Subscription)
        .filter(Subscription.subscription_key == subscription_key)
        .first()
    )
    if not subscription:
        return {"exists": False, "is_active": False}

    subscription.last_checked = datetime.utcnow()
    db.commit()
    return subscription


def deactivate_subscription(db: Session, subscription_key: str):
    subscription = (
        db.query(Subscription)
        .filter(Subscription.subscription_key == subscription_key)
        .first()
    )
    if not subscription:
        return False
    subscription.is_active = False
    db.commit()
    return True
