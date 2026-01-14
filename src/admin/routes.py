from fastapi import APIRouter, Depends, HTTPException
from src.auth.permissions import require_admin
from src.auth.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import get_db
from sqlalchemy import select

admin_router = APIRouter(prefix='/admin',  tags=['Admin Panel'])

@admin_router.get('/users')
async def get_all_users(admin: User = Depends(require_admin),
                        db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()

@admin_router.patch('/users{user_id}/role')
async def change_user_role(user_id: int, new_role:str,
                           admin: User = Depends(require_admin),
                           db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id==user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=404, detail='user not found')
    user.role = new_role
    await db.commit()
    return {"message": f"Role updated to {new_role}"}

@admin_router.delete('/users{user_id}')
async def delete_user(user_id: int, admin: User = Depends(require_admin),
                      db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()
    return {"message": "User deleted"}
