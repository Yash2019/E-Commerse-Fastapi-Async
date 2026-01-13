from fastapi import FastAPI
from src.auth.routes import auth_route
from src.db.main import create_table

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await create_table()

app.include_router(
    auth_route,
    prefix='/auth',
    tags=['Authentication']
)