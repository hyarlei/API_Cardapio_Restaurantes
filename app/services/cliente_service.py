from fastapi import HTTPException
from pymongo import ASCENDING

from app.models.modelagem import Cliente


async def criar_cliente(cliente_data: dict):
    cliente = Cliente(**cliente_data)
    await cliente.insert()
    return cliente


async def listar_clientes(offset: int = 0, limit: int = 10, nome: str = None):
    try:
        pipeline = []

        if nome:
            pipeline.append({"$match": {"nome": {"$regex": nome, "$options": "i"}}})

        pipeline.append(
            {
                "$project": {
                    "_id": {"$toString": "$_id"},
                    "nome": 1,
                    "email": 1,
                    "telefone": 1,
                }
            }
        )

        pipeline.append({"$sort": {"nome": ASCENDING}})
        pipeline.append({"$skip": offset})
        pipeline.append({"$limit": limit})

        clientes = await Cliente.aggregate(pipeline).to_list()

        if not clientes:
            raise HTTPException(status_code=404, detail="Nenhum cliente encontrado")
        return clientes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar clientes: {e}")


async def buscar_cliente(cliente_id: str):
    cliente = await Cliente.get(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente


async def atualizar_cliente(cliente_id: str, cliente_data: dict):
    cliente = await Cliente.get(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    for key, value in cliente_data.items():
        setattr(cliente, key, value)

    await cliente.save()
    return cliente


async def remover_cliente(cliente_id: str):
    cliente = await Cliente.get(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    await cliente.delete()
    return {"message": "Cliente removido com sucesso"}
