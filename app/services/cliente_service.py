from fastapi import HTTPException

from app.models.modelagem import Cliente


async def criar_cliente(cliente_data: dict):
    cliente = Cliente(**cliente_data)
    await cliente.insert()
    return cliente


async def listar_clientes():
    return await Cliente.find_all().to_list()


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
