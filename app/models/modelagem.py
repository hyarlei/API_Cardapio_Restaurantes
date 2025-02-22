from datetime import datetime
from typing import List, Literal, Optional

from beanie import Document
from pydantic import Field


class Cliente(Document):
    nome: str
    email: str
    telefone: Optional[str] = None


class Menu(Document):
    nome: str
    descricao: Optional[str] = None
    preco: float
    tipo: Literal[
        "Entrada", "Principal", "Sobremesa", "Bebida", "Acompanhamento", "Outro"
    ]
    disponivel: bool = True


class Pedido(Document):
    cliente_id: str
    itens_ids: List[str]
    data_pedido: datetime = Field(default_factory=datetime.utcnow)
    status: Literal["pendente", "em preparo", "pronto", "entregue"] = "pendente"
