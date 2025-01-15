from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Menu(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    descricao: str
    preco: float
    tipo: str
    disponivel: bool
    pedidos: List["PedidoItem"] = Relationship(back_populates="menu")