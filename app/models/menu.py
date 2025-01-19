from typing import Optional
from sqlmodel import Field, SQLModel
from enum import Enum
from datetime import datetime

class TipoMenu(str, Enum):
    entrada = "entrada"
    principal = "principal"
    sobremesa = "sobremesa"
    bebida = "bebida"
    acompanhamento = "acompanhamento"
    outro = "outro"

class Menu(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    descricao: str
    preco: float
    tipo: str
    disponivel: bool
    data: datetime