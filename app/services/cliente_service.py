from sqlmodel import Session, select
from app.models.cliente import Cliente
from app.models.pedido import Pedido, PedidoItem
from app.db import engine

def criar_cliente(session: Session, cliente_data: dict):
    with Session(engine) as session:
        cliente = Cliente(**cliente_data)
        session.add(cliente)
        session.commit()
        session.refresh(cliente)
    return cliente

def listar_clientes(session: Session):
    with Session(engine) as session:
        statement = select(Cliente)
        return session.exec(statement).all()

def buscar_cliente(cliente_id: int, session: Session):
    with Session(engine) as session:
        statement = select(Cliente).where(Cliente.id == cliente_id)
        return session.exec(statement).first()

def atualizar_cliente(cliente_id: int, cliente_data: dict, session: Session):
    with Session(engine) as session:
        statement = select(Cliente).where(Cliente.id == cliente_id)
        cliente = session.exec(statement).first()
        for key, value in cliente_data.items():
            setattr(cliente, key, value)
        session.add(cliente)
        session.commit()
        session.refresh(cliente)
    return cliente

def remover_cliente(cliente_id: int, session: Session):
    with Session(engine) as session:
        # Excluir os itens associados aos pedidos do cliente
        pedidos = session.query(Pedido).filter(Pedido.cliente_id == cliente_id).all()
        for pedido in pedidos:
            session.query(PedidoItem).filter(PedidoItem.pedido_id == pedido.id).delete()
        
        # Excluir os pedidos associados ao cliente
        session.query(Pedido).filter(Pedido.cliente_id == cliente_id).delete()
        
        # Excluir o cliente
        statement = select(Cliente).where(Cliente.id == cliente_id)
        cliente = session.exec(statement).first()
        session.delete(cliente)
        session.commit()
        return cliente