from sqlalchemy.orm import Session
from src.auth.models import User
from fastapi import HTTPException, Depends, status
import jwt
from jwt.exceptions import InvalidTokenError
from Config import config
from src.db.main import get_db
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from sqlalchemy import select
from src.auth.logic import get_user
from src.auth.schema import Register
from src.auth.logic import get_pass_hash, authenticate_user, create_access_token, create_refresh_token

oauth_scheme = OAuth2PasswordBearer(tokenUrl='login')

async def get_current_user(token: Annotated[str, Depends(oauth_scheme)],
                     db: Session = Depends(get_db)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could Not Validate the Creds',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try: 
        payload = jwt.decode(token, config.SECREAT_KEY, algorithms=[config.ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise credential_exception
    except InvalidTokenError:
        raise credential_exception
    
    user = get_user(db, username=username)
    if user is None:
        raise credential_exception
    return user

async def registration(user_create: Register, db: Session = Depends(get_db)):
    stmt = select(User).where(User.username == user_create.username)
    result = await db.execute(stmt)
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User already Exists'
        )
    hashed_password = get_pass_hash(user_create.password)

    new_user = User(
        username=user_create.username,
        email=user_create.email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

async def login(username: str, password: str, db: Session = Depends(get_db)):
    user  = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User not Authenticated'
        )
    access_token = create_access_token(
        data = {'sub': user.username}
    )

    refresh_token = create_refresh_token(
        data={'sub': user.username}
    )

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'bearer'
    }


async def refresh_token(token: str, db: Session=Depends(get_db)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could Not Validate the Creds',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        payload = jwt.decode(token, config.SECREAT_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get('sub')
        token_type:str = payload.get('type')

        if username is None or token_type != 'refresh':
            raise credential_exception
            
    except InvalidTokenError:
        raise credential_exception
    
    user = get_user(db, username=username)
    if user is None:
        raise credential_exception

    access_token = create_access_token(data={'sub': user.username})

    return {
        'access_token': access_token,
        'token_type': 'bearer'
        
    }


    




    



        