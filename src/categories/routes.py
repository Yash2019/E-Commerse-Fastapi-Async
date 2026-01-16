from fastapi import APIRouter, HTTPException, Depends
from src.categories.schema import ReadCategory, CreateCategorySchema
from src.categories.logic import Create_Category
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import get_db
from src.auth.dependencies import get_current_user
from src.auth.models import User

category_router = APIRouter(prefix='/category', tags=['Category'])


@category_router.post('/', response_model=ReadCategory)
async def create_category(category_data: CreateCategorySchema, db: AsyncSession = Depends(get_db)):
    return await Create_Category(category_data, db)


