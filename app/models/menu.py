from pydantic import BaseModel

class MenuItemCreate(BaseModel):
    nome: str
    descricao: str
    preco: float
    tipo: str
    disponivel: bool

class MenuItem(MenuItemCreate):
    id: int