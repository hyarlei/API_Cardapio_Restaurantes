from fastapi import APIRouter
from app.models.menu import MenuItemCreate
from app.services.csv_service import criar_menu_item, listar_menu_items

router = APIRouter()

@router.post("/")
async def adicionar_menu_item(item: MenuItemCreate):
    criar_menu_item(item)
    return {"message": "Item adicionado ao menu"}

@router.get("/")
async def obter_menu_items():
    return listar_menu_items()