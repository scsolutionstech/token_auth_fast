# token_auth_fast
<!-- APIs to validate token using FastAPI -->


<!-- FastAPI Authentication and User Management. -->

This project provides a FastAPI-based API for user authentication and management.
It includes user registration, token generation for authentication (access and refresh tokens), and a  subscription key verification system.
 The backend uses SQLAlchemy for database interactions and JOSE for JWT (JSON Web Token) handling.

 <!-- Table of Contents: -->
 <!-- FastAPI Authentication and User Management.. -->
 1.  Features
 2.  Requirements
 3.  Installation
 4.  Configuration
 4.  Usage
 5.  API Endpoints
    1. User Registration
    2. Token Generation
    3. Token Refresh
    4. Subscription Key Verification
    5. User Information

6.  Project Files
   1. main.py
   2. models.py
   3. database.py
   4. schemas.py
   5. utils.py

<!-- Features -->
User Registration:    Allows users to register with a unique username and email.
Token Authentication: Supports OAuth2 with password flow for generating access and refresh tokens.
Token Refresh:        Allows refreshing of access tokens using a refresh token.
User Management:      Allows retrieval of the current user's information.
Subscription
Key Verification:     Verifies the validity of a subscription key.


<!-- Requirements -->

1. Python 3.12.2
2. FastAPI
3. SQLAlchemy
4. JOSE (Python JWT)
5. Uvicorn (for ASGI server)
6. bcrypt (for password hashing)



<!-- 1. Installation -->
1. Clone the repository:
git clone https://github.com/your-username/your-repository.git
cd your-repository

<!-- 2. Create a virtual environment: -->
python -m venv venv

<!-- 3. Install the dependencies: -->
pip install -r requirements.txt

<!-- Usage -->
uvicorn main:app --reload
