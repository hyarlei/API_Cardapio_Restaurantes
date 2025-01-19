from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.pedido import Pedido, PedidoItem
from app.models.menu import Menu
from app.models.cliente import Cliente
from datetime import datetime

def criar_pedido(session: Session, pedido_data: dict):
    try:
        itens_data = pedido_data.pop("itens")
        
        pedido_data["data"] = datetime.fromisoformat(pedido_data["data"])
        
        pedido = Pedido(**pedido_data)
        session.add(pedido)
        session.commit()
        
        total = 0   
        for item in itens_data:
            menu = session.get(Menu, item["menu_id"])
            cliente = session.get(Cliente, item["cliente_id"])
            if not menu:
                raise HTTPException(status_code=404, detail=f"Item do menu com ID {item['menu_id']} não encontrado")

            pedido_item = PedidoItem(
                cliente_id=cliente.id,
                pedido_id=pedido.id,
                menu_id=menu.id,
                quantidade=item["quantidade"]
            )
            session.add(pedido_item)

           
            total += menu.preco * item["quantidade"]

        pedido.total = total
        session.commit()
        session.refresh(pedido)

        return {
            "id": pedido.id,
            "data": pedido.data,
            "total": pedido.total,
            "itens": [{"menu_id": item["menu_id"], "quantidade": item["quantidade"]} for item in itens_data]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar pedido: {e}")

def listar_pedidos(session: Session, offset: int = 0, ano: int = None, limit: int = 100, order_by: str = "id"):
    try:
            statement = select(Pedido).offset(offset).limit(limit)
            if ano:
                statement = statement.where(Pedido.data.like(f"{ano}%"))
            if order_by:
                statement = statement.order_by(getattr(Pedido, order_by))
            pedidos = session.exec(statement).all()
            return pedidos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar pedidos: {e}")
    
def buscar_pedido(session: Session, pedido_id: int):
    try:
            statement = select(Pedido).where(Pedido.id == pedido_id)
            pedido = session.exec(statement).first()
            if not pedido:
                raise HTTPException(status_code=404, detail="Pedido não encontrado")
            return pedido
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar pedido: {e}")

def atualizar_pedido(pedido_id: int, pedido_data: dict, session: Session):
    try:
        pedido = session.get(Pedido, pedido_id)
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        
        for key, value in pedido_data.items():
            if key != "itens" and hasattr(pedido, key):
                setattr(pedido, key, value)
        
        session.commit()
        return pedido
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar pedido: {e}")

def remover_pedido(pedido_id: int, session: Session):
    try:
        pedido = session.get(Pedido, pedido_id)
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")

        session.delete(pedido)
        session.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao remover pedido: {e}")
    