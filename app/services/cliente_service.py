from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.cliente import Cliente
from app.models.pedido import Pedido, PedidoItem

def criar_cliente(session: Session, cliente_data: dict):
    try:
            cliente = Cliente(**cliente_data)
            session.add(cliente)
            session.commit()
            session.refresh(cliente)
            return cliente
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar cliente: {e}")

def listar_clientes(session: Session, offset: int = 0, nome: str = None, limit: int =100, order_by: str = "id"):
    try:
            statement = select(Cliente).offset(offset).limit(limit)
            if nome:
                statement = statement.where(Cliente.nome.contains(nome))
            if order_by:
                statement = statement.order_by(getattr(Cliente, order_by))
            clientes = session.exec(statement).all()
            return clientes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar clientes: {e}")

def buscar_cliente(cliente_id: int, session: Session):
    try:
            cliente = session.get(Cliente, cliente_id)
            if not cliente:
                raise HTTPException(status_code=404, detail="Cliente não encontrado")
            return cliente
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar cliente: {e}")
    
def atualizar_cliente(cliente_id: int, cliente_data: dict, session: Session):
    try:
            cliente = session.exec(select(Cliente).where(Cliente.id == cliente_id)).first()
            for key, value in cliente_data.items():
                setattr(cliente, key, value)
            session.add(cliente)
            session.commit()
            session.refresh(cliente)
            return cliente
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar cliente: {e}")

def remover_cliente(cliente_id: int, session: Session):
    try:
            pedidos = session.query(Pedido).join(PedidoItem).filter(PedidoItem.cliente_id == cliente_id).all()
            for pedido in pedidos:
                session.query(PedidoItem).filter(PedidoItem.pedido_id == pedido.id).delete()
            
            session.query(Pedido).filter(Pedido.id.in_([pedido.id for pedido in pedidos])).delete()
            
            cliente = session.get(Cliente, cliente_id)
            if not cliente:
                raise HTTPException(status_code=404, detail="Cliente não encontrado")
            session.delete(cliente)
            session.commit()
            return cliente
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao remover cliente: {e}")