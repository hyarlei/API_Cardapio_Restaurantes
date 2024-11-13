from fastapi import FastAPI
from app.routes import menu_routes

app = FastAPI()

app.include_router(menu_routes.router, prefix="/menu", tags=["Menu"])