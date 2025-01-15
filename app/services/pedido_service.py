from sqlmodel import Session, select
from app.models.pedido import Pedido, PedidoItem
from app.db import engine
from datetime import datetime

def criar_pedido(session: Session, pedido_data: dict):
    with Session(engine) as session:
        itens_data = pedido_data.pop("itens")
        
        # Converter a string data em um objeto datetime
        pedido_data["data"] = datetime.fromisoformat(pedido_data["data"])
        
        pedido = Pedido(**pedido_data)
        session.add(pedido)
        session.commit()
        session.refresh(pedido)
        
        for item_data in itens_data:
            item_data["pedido_id"] = pedido.id
            pedido_item = PedidoItem(**item_data)
            session.add(pedido_item)
        
        session.commit()
        session.refresh(pedido)
    return pedido

def listar_pedidos(session: Session):
    with Session(engine) as session:
        statement = select(Pedido)
        return session.exec(statement).all()

def buscar_pedido(pedido_id: int, session: Session):
    with Session(engine) as session:
        statement = select(Pedido).where(Pedido.id == pedido_id)
        return session.exec(statement).first()

def atualizar_pedido(pedido_id: int, pedido_data: dict, session: Session):
    with Session(engine) as session:
        statement = select(Pedido).where(Pedido.id == pedido_id)
        pedido = session.exec(statement).first()
        
        # Converter a string data em um objeto datetime, se presente
        if "data" in pedido_data:
            pedido_data["data"] = datetime.fromisoformat(pedido_data["data"])
        
        # Atualizar os atributos do pedido
        for key, value in pedido_data.items():
            if key != "itens":
                setattr(pedido, key, value)
        
        # Atualizar os itens do pedido
        if "itens" in pedido_data:
            # Remover os itens antigos
            session.query(PedidoItem).filter(PedidoItem.pedido_id == pedido_id).delete()
            # Adicionar os novos itens
            for item_data in pedido_data["itens"]:
                item_data["pedido_id"] = pedido.id
                pedido_item = PedidoItem(**item_data)
                session.add(pedido_item)
        
        session.commit()
        session.refresh(pedido)
    return pedido

def remover_pedido(pedido_id: int, session: Session):
    with Session(engine) as session:
        # Excluir os itens associados ao pedido
        session.query(PedidoItem).filter(PedidoItem.pedido_id == pedido_id).delete()
        
        # Excluir o pedido
        statement = select(Pedido).where(Pedido.id == pedido_id)
        pedido = session.exec(statement).first()
        session.delete(pedido)
        session.commit()
        return pedido