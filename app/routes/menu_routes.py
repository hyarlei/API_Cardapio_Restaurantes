from typing import List, Optional

from fastapi import APIRouter, Query

from app.models.modelagem import Menu
from app.services.menu_service import (
    atualizar_menu,
    buscar_menu,
    criar_menu,
    listar_menus,
    remover_menu,
)

router = APIRouter()


@router.post("/", status_code=201)
async def create_menu(menu: Menu):
    return await criar_menu(menu.dict())


@router.get("/{menu_id}")
async def get_menu(menu_id: str):
    return await buscar_menu(menu_id)


@router.get("/", response_model=List[Menu])
async def get_all_menus(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    nome: Optional[str] = Query(default=None),
):
    return await listar_menus(offset=offset, limit=limit, nome=nome)


@router.put("/{menu_id}")
async def update_menu(
    menu_id: str, menu: dict
):  # mudei pra dict, qualquer coisa mudo de volta para o paranetro menu: Menu
    return await atualizar_menu(menu_id, menu.dict())


@router.delete("/{menu_id}")
async def delete_menu(menu_id: str):
    return await remover_menu(menu_id)
