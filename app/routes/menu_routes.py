from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from app.models.menu import MenuItem
from app.services.csv_service import (
    criar_menu_item,
    listar_menu_items,
    atualizar_menu_item,
    remover_item,
    compactar_db,
    buscar_item_por_id,
    obter_menu_hash,
    contar_itens_menu,
)

router = APIRouter()


@router.get("/")
async def obter_menu_items():
    items = listar_menu_items()
    return items


@router.get("/compactar-csv", status_code=status.HTTP_200_OK)
async def compactar_menu_csv():
    compactar_db()
    return FileResponse(
        "app/data/menu.zip", media_type="application/zip", filename="menu.zip"
    )


@router.get("/hash-csv", status_code=status.HTTP_200_OK)
async def obter_menu_hash_csv():
    return obter_menu_hash()


@router.get("/quantidade", status_code=status.HTTP_200_OK)
async def obter_quantidade_itens():
    return contar_itens_menu()


@router.get("/{item_id}", status_code=status.HTTP_200_OK)
async def obter_menu_item(item_id: int):
    try:
        return buscar_item_por_id(item_id)
    except HTTPException as e:
        raise e


@router.post("/", status_code=status.HTTP_201_CREATED)
async def adicionar_menu_item(item: MenuItem):
    criar_menu_item(item)
    return {"message": "Item adicionado ao menu com sucesso"}


@router.put("/{item_id}", status_code=status.HTTP_200_OK)
async def modificar_menu_item(item_id: int, item_atualizado: MenuItem):
    try:
        atualizar_menu_item(item_id, item_atualizado)
        return {"message": "Item modificado no menu com sucesso"}
    except HTTPException as e:
        raise e


@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
async def remover_menu_item(item_id: int):
    try:
        remover_item(item_id)
        return {"message": "Item removido do menu com sucesso"}
    except HTTPException as e:
        raise e
