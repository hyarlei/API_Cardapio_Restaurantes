from pydantic import BaseModel


class MenuItem(BaseModel):
    id: int | None = None
    nome: str
    descricao: str
    preco: float
    tipo: str
    disponivel: bool
