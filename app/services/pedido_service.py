import logging
from datetime import datetime

from bson import ObjectId
from fastapi import HTTPException
from pymongo import ASCENDING

from app.models.modelagem import Cliente, Menu, Pedido


async def criar_pedido(pedido_data: dict):
    cliente = await Cliente.get(ObjectId(pedido_data["cliente_id"]))
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    itens_existentes = []
    for item_id in pedido_data["itens_ids"]:
        item = await Menu.get(ObjectId(item_id))
        if not item:
            raise HTTPException(
                status_code=404, detail=f"Item {item_id} não encontrado"
            )
        itens_existentes.append(item_id)

    pedido = Pedido(
        cliente_id=pedido_data["cliente_id"],
        itens_ids=itens_existentes,
        status=pedido_data.get("status", "pendente"),
    )
    await pedido.insert()
    return pedido


async def listar_pedidos(
    offset: int = 0,
    limit: int = 10,
    cliente_nome: str = None,
    data_inicio: str = None,
    data_fim: str = None,
):
    try:
        pipeline = []

        if cliente_nome:
            pipeline.append(
                {"$match": {"nome": {"$regex": cliente_nome, "$options": "i"}}}
            )

        if data_inicio or data_fim:
            match_stage = {}
            if data_inicio:
                data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
                match_stage["data_pedido"] = {"$gte": data_inicio_dt}
            if data_fim:
                data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
                if "data_pedido" in match_stage:
                    match_stage["data_pedido"]["$lte"] = data_fim_dt
                else:
                    match_stage["data_pedido"] = {"$lte": data_fim_dt}
            pipeline.append({"$match": match_stage})

        pipeline.append(
            {
                "$project": {
                    "_id": {"$toString": "$_id"},
                    "cliente_id": 1,
                    "itens_ids": 1,
                    "data_pedido": 1,
                    "status": 1,
                }
            }
        )

        pipeline.append({"$sort": {"data_pedido": ASCENDING}})
        pipeline.append({"$skip": offset})
        pipeline.append({"$limit": limit})

        pedidos = await Pedido.aggregate(pipeline).to_list()

        return pedidos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar pedidos: {e}")


async def buscar_pedido(pedido_id: str):
    try:
        pedido = await Pedido.get(ObjectId(pedido_id), fetch_links=True)
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")

        cliente = await Cliente.get(pedido.cliente_id)

        itens = [await Menu.get(item_id) for item_id in pedido.itens_ids]

        cliente_dict = cliente.model_dump() if cliente else None
        if cliente_dict:
            cliente_dict["id"] = str(cliente.id)

        return {
            "id": str(pedido.id),
            "cliente": cliente_dict,
            "itens": [
                {
                    "id": str(item.id),
                    "nome": item.nome,
                    "descricao": item.descricao,
                    "preco": item.preco,
                    "tipo": item.tipo,
                    "disponivel": item.disponivel,
                }
                for item in itens
                if item
            ],
            "data_pedido": pedido.data_pedido,
            "status": pedido.status,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar pedido: {e}")


async def atualizar_pedido(pedido_id: str, pedido_data: dict):
    pedido = await Pedido.get(ObjectId(pedido_id))
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    for key, value in pedido_data.items():
        setattr(pedido, key, value)

    await pedido.save()
    return pedido


async def remover_pedido(pedido_id: str):
    pedido = await Pedido.get(ObjectId(pedido_id))
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    await pedido.delete()
    return {"message": "Pedido removido com sucesso"}


async def pratos_mais_vendidos():
    pedidos = await Pedido.find().to_list()
    itens = []
    for pedido in pedidos:
        itens += pedido.itens_ids
    itens_unicos = set(itens)
    pratos = []
    for item in itens_unicos:
        pratos.append({"id": item, "quantidade": itens.count(item)})
    pratos.sort(key=lambda x: x["quantidade"], reverse=True)
    return pratos


async def buscar_pedidos_por_texto(texto: str):
    pedidos = await Pedido.find().to_list()

    pedidos_completos = []
    for pedido in pedidos:
        cliente = await Cliente.get(pedido.cliente_id)
        itens = [await Menu.get(item_id) for item_id in pedido.itens_ids]

        cliente_dict = cliente.model_dump() if cliente else None
        if cliente_dict:
            cliente_dict["id"] = str(cliente.id)

        itens_validos = []
        for item_id, item in zip(pedido.itens_ids, itens):
            if item is None:
                logging.warning(f"Item com ID {item_id} não encontrado.")
                continue  # Pula itens não encontrados

            if texto in item.nome or texto in item.descricao:
                itens_validos.append(
                    {
                        "id": str(item.id),
                        "nome": item.nome,
                        "descricao": item.descricao,
                        "preco": item.preco,
                        "tipo": item.tipo,
                        "disponivel": item.disponivel,
                    }
                )

        if itens_validos:
            pedidos_completos.append(
                {
                    "id": str(pedido.id),
                    "cliente": cliente_dict,
                    "itens": itens_validos,
                    "data_pedido": pedido.data_pedido,
                    "status": pedido.status,
                }
            )

    return pedidos_completos


async def listar_pedidos_com_detalhes(offset: int = 0, limit: int = 10):
    pedidos = await Pedido.find().skip(offset).limit(limit).to_list()

    pedidos_completos = []
    for pedido in pedidos:
        cliente = await Cliente.get(pedido.cliente_id)
        itens = [await Menu.get(item_id) for item_id in pedido.itens_ids]

        cliente_dict = cliente.model_dump() if cliente else None
        if cliente_dict:
            cliente_dict["id"] = str(cliente.id)

        pedidos_completos.append(
            {
                "id": str(pedido.id),
                "cliente": cliente_dict,
                "itens": [
                    {
                        "id": str(item.id),
                        "nome": item.nome,
                        "descricao": item.descricao,
                        "preco": item.preco,
                        "tipo": item.tipo,
                        "disponivel": item.disponivel,
                    }
                    for item in itens
                    if item
                ],
                "data_pedido": pedido.data_pedido,
                "status": pedido.status,
            }
        )

    return pedidos_completos
