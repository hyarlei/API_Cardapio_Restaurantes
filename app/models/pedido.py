from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class Pedido(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cliente_id: int = Field(foreign_key="cliente.id")
    data: datetime
    total: float
    itens: List["PedidoItem"] = Relationship(back_populates="pedido")
    cliente: "Cliente" = Relationship(back_populates="pedidos")

class PedidoItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    pedido_id: int = Field(foreign_key="pedido.id")
    menu_id: int = Field(foreign_key="menu.id")
    quantidade: int
    pedido: "Pedido" = Relationship(back_populates="itens")
    menu: "Menu" = Relationship(back_populates="pedidos")