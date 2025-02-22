from datetime import datetime

from bson import ObjectId
from fastapi import HTTPException

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


async def listar_pedidos():
    pedidos = await Pedido.find(fetch_links=True).to_list()

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
                    for item in itens if item
                ],
                "data_pedido": pedido.data_pedido,
                "status": pedido.status,
            }
        )

    return pedidos_completos


async def buscar_pedido(pedido_id: str):
    try:
        print(f"Buscando pedido com ID: {pedido_id}")  # Depuração

        # Tenta buscar o pedido pelo ID
        pedido = await Pedido.get(ObjectId(pedido_id), fetch_links=True)
        if not pedido:
            print("Pedido não encontrado")  # Depuração
            raise HTTPException(status_code=404, detail="Pedido não encontrado")

        print(f"Pedido encontrado: {pedido}")  # Depuração

        # Tenta buscar o cliente associado ao pedido
        cliente = await Cliente.get(pedido.cliente_id)
        print(f"Cliente encontrado: {cliente}")  # Depuração

        itens = [await Menu.get(item_id) for item_id in pedido.itens_ids]
        print(f"Itens encontrados: {itens}")  # Depuração

        # Converte o cliente para dicionário, se existir
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
                for item in itens if item
            ],
            "data_pedido": pedido.data_pedido,
            "status": pedido.status,
        }
    except Exception as e:
        print(f"Erro ao buscar pedido: {e}")  # Depuração
        raise HTTPException(status_code=500, detail=f"Erro ao buscar pedido: {e}")


async def listar_pedidos_por_data(data_inicio: str, data_fim: str):
    try:
        data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
        data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")

        print(f"Buscando pedidos entre {data_inicio_dt} e {data_fim_dt}")

        pedidos = await Pedido.find(
            Pedido.data_pedido >= data_inicio_dt, Pedido.data_pedido <= data_fim_dt
        ).to_list()

        print(f"Pedidos encontrados: {len(pedidos)}")

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
                        for item in itens if item
                    ],
                    "data_pedido": pedido.data_pedido,
                    "status": pedido.status,
                }
            )

        return pedidos_completos
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao listar pedidos por data: {e}"
        )


async def listar_pedidos_ordenados(campo: str, ordem: int):
    try:
        if ordem not in [1, -1]:
            raise ValueError("Ordem deve ser 1 (ascendente) ou -1 (descendente)")

        pedidos = await Pedido.find().sort([(campo, ordem)]).to_list()

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
                        for item in itens if item
                    ],
                    "data_pedido": pedido.data_pedido,
                    "status": pedido.status,
                }
            )

        return pedidos_completos
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao listar pedidos ordenados: {e}"
        )


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


async def clientes_vip():
    try:
        pedidos = await Pedido.find().to_list()
        clientes = {}
        for pedido in pedidos:
            if pedido.cliente_id in clientes:
                clientes[pedido.cliente_id] += sum(
                    [(await Menu.get(item_id)).preco for item_id in pedido.itens_ids]
                )
            else:
                clientes[pedido.cliente_id] = sum(
                    [(await Menu.get(item_id)).preco for item_id in pedido.itens_ids]
                )
        clientes = [
            {"cliente_id": str(cliente_id), "total_gasto": total_gasto}
            for cliente_id, total_gasto in clientes.items()
        ]
        clientes.sort(key=lambda x: x["total_gasto"], reverse=True)
        return clientes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar clientes VIP: {e}")


async def buscar_pedidos_por_texto(texto: str):
    pedidos = await Pedido.find().to_list()

    pedidos_completos = []
    for pedido in pedidos:
        cliente = await Cliente.get(pedido.cliente_id)
        itens = [await Menu.get(item_id) for item_id in pedido.itens_ids]

        cliente_dict = cliente.model_dump() if cliente else None
        if cliente_dict:
            cliente_dict["id"] = str(cliente.id)

        for item in itens:
            if texto in item.nome or texto in item.descricao:
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
                        ],
                        "data_pedido": pedido.data_pedido,
                        "status": pedido.status,
                    }
                )
                break

    return pedidos_completos


async def listar_pedidos_com_detalhes():
    pedidos = await Pedido.find().to_list()

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
                    for item in itens if item
                ],
                "data_pedido": pedido.data_pedido,
                "status": pedido.status,
            }
        )

    return pedidos_completos
