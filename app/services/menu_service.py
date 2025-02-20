from fastapi import HTTPException
from app.models.modelagem import Menu
from typing import List, Optional

async def criar_menu(menu_data: dict):
    try:
        menu = Menu(**menu_data)
        await menu.insert()
        return menu
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar menu: {e}")

async def listar_menus(offset: int = 0, limit: int = 10, nome: Optional[str] = None):
    try:
        filtros = {}

        if nome:
            filtros["nome"] = {"$regex": nome, "$options": "i"}  # Busca case-insensitive

        menus = await Menu.find(filtros).skip(offset).limit(limit).to_list()
        return menus
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar menus: {str(e)}")

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