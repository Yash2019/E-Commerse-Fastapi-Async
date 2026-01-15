from fastapi import APIRouter, Depends
from src.auth.models import User
from src.auth.dependencies import get_current_user

user_router = APIRouter(prefix='/user', tags=['user Panel'])

@user_router.get('/profile')
async def get_profile(user: User = Depends(get_current_user)):
    return {'id': user.id, 'username': user.username, 'email': user.email, 'role': user.role}
