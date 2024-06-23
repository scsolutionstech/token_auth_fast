from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from controller import (
    register_user,
    authenticate_user,
    create_tokens,
    refresh_access_token,
    check_subscription,
    deactivate_subscription,
)
from database import get_db, engine
from deps import get_current_user
from models import User, Base
from schemas import (
    UserRegister,
    TokenRefresh,
    SubscriptionCheck,
    SubscriptionDeactivate,
)
app = FastAPI()
Base.metadata.create_all(bind=engine)


auth_router = APIRouter()
subscription_router = APIRouter()
app.include_router(auth_router)
app.include_router(subscription_router)


@auth_router.post("/register", summary="Create a new user", tags=["User"])
def register(user: UserRegister, db: Session = Depends(get_db)):
    """Register a new user."""

    db_user = register_user(db, user.username, user.password)
    return {"username": db_user.username}


@auth_router.post("/login", tags=["User"])
def login(user: OAuth2PasswordRequestForm, db: Session = Depends(get_db)) -> dict[str, str]:
    """Authenticate a user and return tokens."""
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
    """Refresh the access token."""
    new_tokens = refresh_access_token(token.refresh_token)
    return new_tokens


@subscription_router.post("/check")
def check(
    subscription: SubscriptionCheck,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Check if a subscription is active."""
    result = check_subscription(db, subscription.subscription_key)
    return result.__dict__() if result else {"exists": False, "is_active": False}


@subscription_router.post("/deactivate")
def deactivate(
    subscription: SubscriptionDeactivate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Deactivate a subscription."""
    deactivate_subscription(db, subscription.subscription_key)
    return {"message": "Subscription deactivated"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)