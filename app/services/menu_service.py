from fastapi import HTTPException
from pymongo import ASCENDING

from app.models.modelagem import Menu


async def criar_menu(menu_data: dict):
    try:
        menu = Menu(**menu_data)
        await menu.insert()
        return menu
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar menu: {e}")


async def listar_menus(offset: int = 0, limit: int = 10, nome: str = None):
    try:
        pipeline = []

        if nome:
            pipeline.append({"$match": {"nome": {"$regex": nome, "$options": "i"}}})

        pipeline.append(
            {
                "$project": {
                    "_id": {"$toString": "$_id"},
                    "nome": 1,
                    "descricao": 1,
                    "preco": 1,
                    "tipo": 1,
                }
            }
        )

        pipeline.append({"$sort": {"nome": ASCENDING}})
        pipeline.append({"$skip": offset})
        pipeline.append({"$limit": limit})

        menus = await Menu.aggregate(pipeline).to_list()

        return menus
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar menus: {e}")


async def buscar_menu(menu_id: str):
    try:
        menu = await Menu.get(menu_id)
        if not menu:
            raise HTTPException(status_code=404, detail="Menu não encontrado")
        return menu
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar menu: {e}")


async def atualizar_menu(menu_id: str, menu_data: dict):
    try:
        menu = await Menu.get(menu_id)
        if not menu:
            raise HTTPException(status_code=404, detail="Menu não encontrado")

        await menu.set(menu_data)
        return menu
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar menu: {e}")


async def remover_menu(menu_id: str):
    try:
        menu = await Menu.get(menu_id)
        if not menu:
            raise HTTPException(status_code=404, detail="Menu não encontrado")

        await menu.delete()
        return {"message": "Menu removido com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao remover menu: {e}")
