from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import User, Subscription
from utils import verify_password, get_password_hash, create_access_token, create_refresh_token
from datetime import datetime, timedelta
from jose import jwt
from utils import SECRET_KEY, ALGORITHM

def register_user(db: Session, username: str, password: str):
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

def create_tokens(user_id: int):
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
    subscriptions = db.query(Subscription).filter(Subscription.subscription_key == subscription_key).all()
    if not subscriptions:
        return {"exists": False, "is_active": False}
    
    for subscription in subscriptions:
        if subscription.expiry_date < datetime.utcnow() or not subscription.is_active:
            subscription.is_active = False
            db.commit()
        else:
            subscription.last_checked = datetime.utcnow()
            db.commit()
            return {"exists": True, "is_active": True}

    return {"exists": True, "is_active": False}

def deactivate_subscription(db: Session, subscription_key: str):
    subscriptions = db.query(Subscription).filter(Subscription.subscription_key == subscription_key).all()
    for subscription in subscriptions:
        subscription.is_active = False
    db.commit()
