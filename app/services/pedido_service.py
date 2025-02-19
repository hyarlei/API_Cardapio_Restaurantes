from fastapi import HTTPException
from app.models.modelagem import Pedido, Cliente, Menu
from bson import ObjectId

async def criar_pedido(pedido_data: dict):
    # Verifica se o Cliente existe
    cliente = await Cliente.get(ObjectId(pedido_data["cliente_id"]))
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    # Verifica se os Itens existem
    itens_existentes = []
    for item_id in pedido_data["itens_ids"]:
        item = await Menu.get(ObjectId(item_id))
        if not item:
            raise HTTPException(status_code=404, detail=f"Item {item_id} não encontrado")
        itens_existentes.append(item_id)  # Armazena apenas os IDs

    # Cria o Pedido com os IDs
    pedido = Pedido(
        cliente_id=pedido_data["cliente_id"],
        itens_ids=itens_existentes,
        status=pedido_data.get("status", "pendente")
    )
    await pedido.insert()
    return pedido

async def listar_pedidos():
    pedidos = await Pedido.find(fetch_links=True).to_list()

    # Enriquecer os pedidos com os dados completos do Cliente e dos Itens
    pedidos_completos = []
    for pedido in pedidos:
        cliente = await Cliente.get(ObjectId(pedido.cliente_id))
        itens = [await Menu.get(ObjectId(item_id)) for item_id in pedido.itens_ids]

        pedidos_completos.append({
            "id": str(pedido.id),
            "cliente": cliente.dict() if cliente else None,
            "itens": [item.dict() for item in itens if item],
            "data_pedido": pedido.data_pedido,
            "status": pedido.status
        })
    
    return pedidos_completos

async def buscar_pedido(pedido_id: str):
    pedido = await Pedido.get(ObjectId(pedido_id), fetch_links=True)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    # Buscar dados completos do Cliente e dos Itens
    cliente = await Cliente.get(ObjectId(pedido.cliente_id))
    itens = [await Menu.get(ObjectId(item_id)) for item_id in pedido.itens_ids]

    return {
        "id": str(pedido.id),
        "cliente": cliente.dict() if cliente else None,
        "itens": [item.dict() for item in itens if item],
        "data_pedido": pedido.data_pedido,
        "status": pedido.status
    }

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
