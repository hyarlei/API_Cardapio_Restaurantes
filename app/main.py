from fastapi import FastAPI

from app.routes.cliente_routes import router as cliente_router
from app.routes.menu_routes import router as menu_router
from app.routes.pedido_routes import router as pedido_router
from init_db import init_db

app = FastAPI()

@app.on_event("startup")
async def startup():
    await init_db()

app.include_router(cliente_router, prefix="/cliente", tags=["Cliente"])
app.include_router(pedido_router, prefix="/pedido", tags=["Pedido"])
app.include_router(menu_router, prefix="/menu", tags=["Menu"])