from pydantic import BaseModel
from typing import Literal

class MenuItem(BaseModel):
    id: int | None = None
    nome: str
    descricao: str
    preco: float
    tipo: Literal["entrada", "principal", "sobremesa", "bebida", "acompanhamento", "outro"]
    disponivel: bool