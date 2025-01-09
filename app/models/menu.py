from pydantic import BaseModel, Field
from typing import Optional

class MenuItem(BaseModel):
    id: Optional[int] = Field(None, description="ID único do item")
    nome: str = Field(..., min_length=3, max_length=100, description="Nome do item")
    descricao: Optional[str] = Field(None, max_length=250, description="Descrição do item")
    preco: float = Field(..., ge=0, description="Preço do item")
    tipo: str = Field(..., description="Tipo do prato (ex.: entrada, prato principal, sobremesa)")
    disponivel: bool = Field(True, description="Disponibilidade do item no menu")