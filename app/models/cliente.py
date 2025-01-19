from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel


class Cliente(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    email: str
    telefone: str
    pedidos: List["PedidoItem"] = Relationship(back_populates="cliente")