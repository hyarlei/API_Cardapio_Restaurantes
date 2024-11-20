from fastapi import APIRouter
from fastapi.responses import FileResponse
from app.models.menu import MenuItem
from app.services.csv_service import criar_menu_item, listar_menu_items, atualizar_menu_item, remover_item, compactar_csv, buscar_item_por_id, obter_menu_hash

router = APIRouter()

@router.get("/")
async def obter_menu_items():
    return listar_menu_items()

@router.post("/")
async def adicionar_menu_item(item: MenuItem):
    criar_menu_item(item)
    return {"message": "Item adicionado ao menu"}

@router.put("/{item_id}")
async def modificar_menu_item(item_id: int, item_atualizado: MenuItem):
    atualizar_menu_item(item_id, item_atualizado)
    return {"message": "Item modificado no menu"}

@router.delete("/{item_id}")
async def remover_menu_item(item_id: int):
    remover_item(item_id)
    return {"message": "Item removido do menu"}

@router.get("/compactar-csv")
async def compactar_menu_csv():
    compactar_csv()
    return FileResponse("app/data/menu.zip", media_type="application/zip", filename="menu.zip")

@router.get("/{item_id}")
async def obter_menu_item(item_id: int):
    return buscar_item_por_id(item_id)

@router.get("/hash-csv")
async def obter_menu_hash_csv():
    return obter_menu_hash()
