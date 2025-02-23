from typing import Optional

from fastapi import APIRouter, Query

from app.models.modelagem import Pedido
from app.services.pedido_service import (
    atualizar_pedido,
    buscar_pedido,
    buscar_pedidos_por_texto,
    criar_pedido,
    listar_pedidos,
    listar_pedidos_com_detalhes,
    pratos_mais_vendidos,
    remover_pedido,
)

router = APIRouter()


@router.post("/", status_code=201)
async def create_pedido(pedido: Pedido):
    return await criar_pedido(pedido.model_dump())


@router.get("/")
async def get_pedidos(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    cliente_nome: Optional[str] = Query(default=None),
    data_inicio: Optional[str] = Query(default=None),
    data_fim: Optional[str] = Query(default=None),
):
    return await listar_pedidos(
        offset=offset,
        limit=limit,
        cliente_nome=cliente_nome,
        data_inicio=data_inicio,
        data_fim=data_fim,
    )


@router.get("/pratos_mais_vendidos")
async def get_pratos_mais_vendidos():
    return await pratos_mais_vendidos()


@router.get("/pedidos_com_detalhes")
async def get_pedidos_com_detalhes(
    offset: int = Query(0, ge=0), limit: int = Query(10, le=100)
):
    return await listar_pedidos_com_detalhes(offset=offset, limit=limit)


@router.get("/buscar_pedidos_por_texto")
async def get_pedidos_por_texto(texto: str):
    return await buscar_pedidos_por_texto(texto)


@router.get("/{pedido_id}")
async def get_pedido(pedido_id: str):
    return await buscar_pedido(pedido_id)


@router.put("/{pedido_id}")
async def update_pedido(pedido_id: str, pedido_data: Pedido):
    return await atualizar_pedido(pedido_id, pedido_data)


@router.delete("/{pedido_id}")
async def delete_pedido(pedido_id: str):
    return await remover_pedido(pedido_id)
