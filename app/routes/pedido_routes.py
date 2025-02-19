from fastapi import APIRouter
from app.services.pedido_service import criar_pedido, listar_pedidos, buscar_pedido, atualizar_pedido, remover_pedido

router = APIRouter()

@router.post("/pedido/")
async def create_pedido(pedido_data: dict):
    return await criar_pedido(pedido_data)

@router.get("/pedido/")
async def get_pedidos():
    return await listar_pedidos()

@router.get("/pedido/{pedido_id}")
async def get_pedido(pedido_id: str):
    return await buscar_pedido(pedido_id)

@router.put("/pedido/{pedido_id}")
async def update_pedido(pedido_id: str, pedido_data: dict):
    return await atualizar_pedido(pedido_id, pedido_data)

@router.delete("/pedido/{pedido_id}")
async def delete_pedido(pedido_id: str):
    return await remover_pedido(pedido_id)
