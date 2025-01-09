from fastapi import FastAPI
from app.routes.menu_routes import router as menu_router
from app.services.csv_service import init_db

app = FastAPI()

init_db()

# Incluindo o roteador
app.include_router(menu_router, prefix="/menu", tags=["Menu"])
