from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class Register(BaseModel):
    username: str
    email: str
    password: str

class UserResponce(BaseModel):
    username: str
    