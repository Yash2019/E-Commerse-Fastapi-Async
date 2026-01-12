from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from src.auth.models import User
from fastapi import HTTPException
import jwt
from datetime import datetime, timedelta, timezone
from Config import config

password_hash = PasswordHash.recommended()

def verify_password(plain_password: str, hashed_password: str):
    return password_hash.verify(plain_password, hashed_password)

def get_pass_hash(password: str):
    return password_hash.hash(password)

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username:str, password: str):
    user = get_user(db, username)
    if not user:
        raise HTTPException(status_code=404, detail='User Not Found')
    if not verify_password(password, user.password):
        raise HTTPException(status_code=404, detail='User not Verifed')
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    if 'sub' not in data:
        raise ValueError('Token Payload must include sub')
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) +  expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, config.SECREAT_KEY, config.ALGORITHM)

def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({'exp': expire, 'type': 'refresh'})
    encode_jwt = jwt.encode(to_encode, config.SECREAT_KEY, algorithm=config.ALGORITHM)
    return encode_jwt


    
    