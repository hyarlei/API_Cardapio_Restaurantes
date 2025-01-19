from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

class PedidoItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    pedido_id: int = Field(foreign_key="pedido.id")
    menu_id: int = Field(foreign_key="menu.id")
    cliente_id: int = Field(foreign_key="cliente.id")
    quantidade: int

    cliente: "Cliente" = Relationship()
    menu: "Menu" = Relationship()

class Pedido(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    total: Optional[float] = None
    pedido_items: List[PedidoItem] = Relationship(cascade_delete=True)
    data: datetime