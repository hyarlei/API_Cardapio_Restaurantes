from fastapi import APIRouter, Query

from app.services.pedido_service import (
    atualizar_pedido,
    buscar_pedido,
    buscar_pedidos_por_texto,
    clientes_vip,
    criar_pedido,
    listar_pedidos,
    listar_pedidos_com_detalhes,
    listar_pedidos_ordenados,
    listar_pedidos_por_data,
    pratos_mais_vendidos,
    remover_pedido,
)

router = APIRouter()


@router.post("/")
async def create_pedido(pedido_data: dict):
    return await criar_pedido(pedido_data)


@router.get("/")
async def get_pedidos():
    return await listar_pedidos()


@router.get("/pedidos_por_data")
async def get_pedidos_por_data(
    data_inicio: str = Query(...), data_fim: str = Query(...)
):
    return await listar_pedidos_por_data(data_inicio, data_fim)


@router.get("/ordenados")
async def get_pedidos_ordenados(campo: str, ordem: int):
    return await listar_pedidos_ordenados(campo, ordem)


@router.get("/pratos_mais_vendidos")
async def get_pratos_mais_vendidos():
    return await pratos_mais_vendidos()


@router.get("/clientes_vip")
async def get_clientes_vip():
    return await clientes_vip()


@router.get("/pedidos_com_detalhes")
async def get_pedidos_com_detalhes():
    return await listar_pedidos_com_detalhes()


@router.get("/buscar_pedidos_por_texto")
async def get_pedidos_por_texto(texto: str):
    return await buscar_pedidos_por_texto(texto)


@router.get("/{pedido_id}")
async def get_pedido(pedido_id: str):
    return await buscar_pedido(pedido_id)


@router.put("/{pedido_id}")
async def update_pedido(pedido_id: str, pedido_data: dict):
    return await atualizar_pedido(pedido_id, pedido_data)


@router.delete("/{pedido_id}")
async def delete_pedido(pedido_id: str):
    return await remover_pedido(pedido_id)
