from typing import Optional

from fastapi import APIRouter, Query

from app.models.modelagem import Cliente
from app.services.cliente_service import (
    atualizar_cliente,
    buscar_cliente,
    criar_cliente,
    listar_clientes,
    remover_cliente,
)

router = APIRouter()


@router.post("/", status_code=201)
async def create_cliente(cliente: Cliente):
    return await criar_cliente(cliente.model_dump())


@router.get("/")
async def get_all_clientes(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    nome: Optional[str] = Query(default=None),
):
    return await listar_clientes(offset=offset, limit=limit, nome=nome)


@router.get("/{cliente_id}")
async def get_cliente(cliente_id: str):
    return await buscar_cliente(cliente_id)


@router.put("/{cliente_id}")
async def update_cliente(cliente_id: str, cliente: Cliente):
    return await atualizar_cliente(cliente_id, cliente)


@router.delete("/{cliente_id}")
async def delete_cliente(cliente_id: str):
    return await remover_cliente(cliente_id)
