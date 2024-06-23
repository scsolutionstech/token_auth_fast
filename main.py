from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from utils import hash_password, verify_password, create_access_token
from schemas import TokenOut, UserOut, UserCreate, SubscriptionBase, TokenPayload
import models

from database import get_db, engine
from deps import get_current_user

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = (
        db.query(models.User)
        .filter(
            (models.User.username == user.username) | (models.User.email == user.email)
        )
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username or email already exists",
        )

    hashed_password = hash_password(user.password)
    db_user = models.User(
        username=user.username, email=user.email, password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# token api
@app.post("/token", response_model=TokenOut)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = (
        db.query(models.User).filter(models.User.username == form_data.username).first()
    )
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token = create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


# generate refresh tokens api
@app.post("/refresh", response_model=TokenOut)
def refresh_access_token(refresh_token: str, db: Session = Depends(get_db)):
    try:
        payload = verify_token(
            refresh_token,
            token_type="refresh",
            secret_key=SECRET_KEY,
            algorithm=ALGORITHM,
        )
    except HTTPException as e:
        raise e

    user = db.query(models.User).filter(models.User.id == payload["user_id"]).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user"
        )

    new_refresh_token = create_refresh_token(data={"user_id": user.id})
    return {"refresh_token": new_refresh_token, "token_type": "bearer"}


# match subscription keys api
@app.post("/subscription-keys/{key}")
def check_subscription_key(
    key: str, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    subscription = (
        db.query(models.Subscription).filter(models.Subscription.key == key).first()
    )
    if subscription:
        return {"message": "Key matched successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Subscription key not found"
        )


# show user details api
@app.get("/users/me", response_model=UserOut)
def read_users_me(current_user: UserOut = Depends(get_current_user)):
    return current_user


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
