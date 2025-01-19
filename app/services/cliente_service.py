from fastapi import HTTPException, Query
from sqlmodel import Session, select
from app.models.cliente import Cliente
from app.models.pedido import Pedido
from app.models.menu import Menu
from app.db import engine

def criar_cliente(session: Session, cliente_data: dict):
    try:
        with Session(engine) as session:
            cliente = Cliente(**cliente_data)
            session.add(cliente)
            session.commit()
            session.refresh(cliente)
        return cliente
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar cliente: {e}")

def listar_clientes(session: Session, offset: int = 0, titulo: str = None, limit: int = Query(default=10, le=100)):
    try:
        with Session(engine) as session:
            statement = select(Cliente).offset(offset).limit(limit)
            if titulo:
                statement = statement.where(Cliente.nome.contains(titulo))
            clientes = session.exec(statement).all()
            return clientes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar clientes: {e}")

def buscar_cliente(cliente_id: int, session: Session):
    try:
        with Session(engine) as session:
            cliente = session.get(Cliente, cliente_id)
            if not cliente:
                raise HTTPException(status_code=404, detail="Cliente não encontrado")
            return cliente
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar cliente: {e}")

def atualizar_cliente(cliente_id: int, cliente_data: dict, session: Session):
    try:
        with Session(engine) as session:
            cliente = session.exec(select(Cliente).where(Cliente.id == cliente_id)).first()
            for key, value in cliente_data.items():
                setattr(cliente, key, value)
            session.add(cliente)
            session.commit()
            session.refresh(cliente)
        return cliente
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar cliente: {e}")

def remover_cliente(cliente_id: int, session: Session):
    try:
        with Session(engine) as session:
            # Excluir os itens associados aos pedidos do cliente
            pedidos = session.query(Pedido).filter(Pedido.cliente_id == cliente_id).all()
            for pedido in pedidos:
                session.query(Menu).filter(Menu.pedido_id == pedido.id).delete()
            
            # Excluir os pedidos associados ao cliente
            session.query(Pedido).filter(Pedido.cliente_id == cliente_id).delete()
            
            # Excluir o cliente
            cliente = session.get(Cliente, cliente_id)
            if not cliente:
                raise HTTPException(status_code=404, detail="Cliente não encontrado")
            session.delete(cliente)
            session.commit()
            return cliente
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao remover cliente: {e}")