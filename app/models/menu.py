from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from enum import Enum

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