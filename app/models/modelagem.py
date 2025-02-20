from beanie import Document
from pydantic import BaseModel
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime

class Cliente(Document):
    nome: str
    email: str
    telefone: Optional[str] = None

class Menu(Document):
    nome: str
    descricao: Optional[str] = None
    preco: float
    tipo: Literal["Entrada", "Principal", "Sobremesa", "Bebida", "Acompanhamento", "Outro"]
    disponivel: bool = True

class Pedido(Document):
    cliente_id: str
    itens_ids: List[str]
    data_pedido: datetime = Field(default_factory=datetime.utcnow)
    status: Literal['pendente', 'em preparo', 'pronto', 'entregue'] = 'pendente'