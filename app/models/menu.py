from pydantic import BaseModel

class MenuItem(BaseModel):
    nome: str
    descricao: str
    preco: float
    tipo: str  #'bebida', 'sobremesa...'
    disponivel: bool