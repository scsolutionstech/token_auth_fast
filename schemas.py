from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True  

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

    class Config:
        from_attributes = True  

class successresponse(BaseModel):
    massage: str ="signup successful"
