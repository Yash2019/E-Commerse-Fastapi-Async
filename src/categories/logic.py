from fastapi import HTTPException, Depends, status
from src.categories.models import Categories as db_Category
from src.categories.schema import ReadCategory, UpdateCategory
from src.db.main import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def CreateCategory(task: ReadCategory, db : AsyncSession):
    new_category = await db_Category(
        name = task.name
    )
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return new_category

async def AllCategories(db: AsyncSession):
    result = await db.execute(select(db_Category))
    return result.scalars().all()

async def OneCategory(cat_id: int, db: AsyncSession):
    stmt = select(db_Category).where(db_Category.id == cat_id)
    result = await db.execute(stmt)
    return result.scalars().first()

async def UpdateCategory(task: UpdateCategory, db: AsyncSession, cat_id: int):
    update = await OneCategory(cat_id, db)
    if not update:
        return None
    if task.name is not None:
        update.name =  task.name
    if task.parent_id is not None:
        update.parent_id = task.parent_id
    await db.commit()
    await db.refresh(update)
    return update

async def DeleteCategory(cat_id: int, db: AsyncSession):
    delet = await OneCategory(cat_id, db)
    if not delet:
        return None
    await db.delete(delet)
    await db.commit()
    return True
