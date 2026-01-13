from fastapi import FastAPI, APIRouter, Depends
from src.auth.dependencies import registration, login, refresh_token
from src.auth.schema import UserResponce, Register, Token
from src.db.main import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm


auth_route = APIRouter()


@auth_route.post('/register', response_model=UserResponce)
async def Registration(task: Register, db: AsyncSession = Depends(get_db)):
    return await registration(task, db)

@auth_route.post('/login')
async def login_endpoint(form_data: OAuth2PasswordRequestForm = Depends(), 
                db: AsyncSession = Depends(get_db)):
    return await login(
        db=db,
        username=form_data.username,
        password=form_data.password
    )

@auth_route.post('/refresh', response_model=Token)
async def refresh_token_endpoint(token: str, db: AsyncSession = Depends(get_db)):
    return await refresh_token(token, db)
