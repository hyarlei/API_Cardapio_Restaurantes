from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.models.modelagem import Cliente
from app.services.cliente_service import criar_cliente, listar_clientes, buscar_cliente, atualizar_cliente, remover_cliente

router = APIRouter()

@router.post("/", status_code=201)
async def create_cliente(cliente: Cliente):
    return await criar_cliente(cliente.dict())

@router.get("/{cliente_id}")
async def get_cliente(cliente_id: str):
    return await buscar_cliente(cliente_id)

@router.get("/")
async def get_all_clientes():
    return await listar_clientes()

@router.put("/{cliente_id}")
async def update_cliente(cliente_id: str, cliente: dict):
    return await atualizar_cliente(cliente_id, cliente)

@router.delete("/{cliente_id}")
async def delete_cliente(cliente_id: str):
    return await remover_cliente(cliente_id)