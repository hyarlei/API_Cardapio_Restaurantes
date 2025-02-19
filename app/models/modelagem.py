from beanie import Document
from pydantic import BaseModel
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime

# Definição do modelo Cliente
class Cliente(Document):
    nome: str
    email: str
    telefone: Optional[str] = None

# Modelo Menu
class Menu(Document):
    nome: str
    descricao: Optional[str] = None
    preco: float
    tipo: Literal["Entrada", "Principal", "Sobremesa", "Bebida", "Acompanhamento", "Outro"]
    disponivel: bool = True

# Modelo Pedido atualizado (agora com IDs em vez de objetos)
class Pedido(Document):
    cliente_id: str  # Apenas o ID do Cliente
    itens_ids: List[str]  # Lista de IDs do Menu
    data_pedido: datetime = Field(default_factory=datetime.utcnow)
    status: Literal['pendente', 'em preparo', 'pronto', 'entregue'] = 'pendente'