from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlmodel import Session
from app.db import get_session
from app.services.menu_sevice import (
    criar_menu_item,
    listar_menu_items,
    buscar_menu_item,
    atualizar_menu_item,
    remover_menu_item,
)
from app.models.menu import Menu

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_menu(menu_data: dict, session: Session = Depends(get_session)):
    criar_menu_item(session, menu_data)
    return {"message": "Item adicionado ao menu com sucesso"}

@router.get("/{item_id}", status_code=status.HTTP_200_OK)
async def read_menu(item_id: int, session: Session = Depends(get_session)):
    item = buscar_menu_item(item_id, session)
    if item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return item

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Menu])
async def read_menu_items(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    titulo: str = Query(None),
    ano: int = Query(None),
    session: Session = Depends(get_session)
):
    return listar_menu_items(session, offset=offset, limit=limit, titulo=titulo, ano=ano)

@router.put("/{item_id}", status_code=status.HTTP_200_OK)
async def update_menu(item_id: int, menu_data: dict, session: Session = Depends(get_session)):
    item = atualizar_menu_item(item_id, menu_data, session)
    if item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return {"message": "Item atualizado com sucesso"}

@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
async def delete_menu(item_id: int, session: Session = Depends(get_session)):
    item = remover_menu_item(item_id, session)
    if item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return {"message": "Item removido com sucesso"}