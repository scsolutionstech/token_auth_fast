# # tests/test_main.py

# import json
# import pytest
# from fastapi.testclient import TestClient
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from database import Base, SessionLocal, engine
# from main import app
# from models import User
# from utils import hash_password


# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base.metadata.create_all(bind=engine)


# @pytest.fixture(scope="module")
# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# def test_register_user(override_get_db):
#     client = TestClient(app)
#     response = client.post(
#         "/register",
#         json={"username": "testuser", "email": "testuser@example.com", "password": "testpassword"},
#     )
#     assert response.status_code == 200
#     assert response.json()["username"] == "testuser"
#     assert response.json()["email"] == "testuser@example.com"


# def test_login_for_access_token(override_get_db):
#     client = TestClient(app)
    
#     register_response = client.post(
#         "/register",
#         json={"username": "testuser", "email": "testuser@example.com", "password": "testpassword"},
#     )
#     assert register_response.status_code == 200

   
#     login_response = client.post(
#         "/token",
#         data={"username": "testuser@example.com", "password": "testpassword"},
#     )
#     assert login_response.status_code == 200
#     assert "access_token" in login_response.json()
#     assert login_response.json()["token_type"] == "bearer"

# # Test protected endpoint
# def test_read_users_me(override_get_db):
#     client = TestClient(app)
#     # Register a user first
#     register_response = client.post(
#         "/register",
#         json={"username": "testuser", "email": "testuser@example.com", "password": "testpassword"},
#     )
#     assert register_response.status_code == 200

   
#     login_response = client.post(
#         "/token",
#         data={"username": "testuser@example.com", "password": "testpassword"},
#     )
#     assert login_response.status_code == 200
#     access_token = login_response.json()["access_token"]

  
#     headers = {"Authorization": f"Bearer {access_token}"}
#     protected_response = client.get("/users/me", headers=headers)
#     assert protected_response.status_code == 200
#     assert protected_response.json()["username"] == "testuser"
#     assert protected_response.json()["email"] == "testuser@example.com"


# if __name__ == "__main__":
#     pytest.main()
