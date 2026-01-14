from fastapi import FastAPI
from src.auth.routes import auth_route
from src.db.main import create_table
from src.admin.routes import admin_router
from src.users.routes import user_router

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await create_table()

app.include_router(
    auth_route,
    prefix='/auth',
    tags=['Authentication']
)

app.include_router(admin_router)
app.include_router(user_router)