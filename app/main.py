from fastapi import FastAPI
from app.routes.menu_routes import router as menu_router
from app.routes.cliente_routes import router as cliente_router
from app.routes.pedido_routes import router as pedido_router
from app.services.menu_sevice import init_db

app = FastAPI()

init_db()

# Incluindo o roteador
app.include_router(menu_router, prefix="/menu", tags=["Menu"])
app.include_router(cliente_router, prefix="/cliente", tags=["Cliente"])
app.include_router(pedido_router, prefix="/pedido", tags=["Pedido"])
