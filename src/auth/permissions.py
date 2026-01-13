from src.auth.dependencies import get_current_user
from fastapi import Depends
from src.auth.models import User, UserRole
from fastapi import HTTPException, status

async def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(status_code=403, detail='Admin Access Required')
    return current_user