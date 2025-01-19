from fastapi import HTTPException, Query
from sqlmodel import Session, select
from app.models.pedido import Pedido, PedidoItem
from app.models.menu import Menu
from app.models.cliente import Cliente
from app.db import engine
from datetime import datetime

def criar_pedido(session: Session, pedido_data: dict):
    try:
        # Extrair os dados dos itens do pedido
        itens_data = pedido_data.pop("itens")
        
        # Converter a string de data em um objeto datetime
        pedido_data["data"] = datetime.fromisoformat(pedido_data["data"])
        
        # Criar o objeto Pedido
        pedido = Pedido(**pedido_data)
        session.add(pedido)
        session.commit()  # Salva o pedido para gerar o ID do pedido
        
        # Associar itens ao pedido
        total = 0
        for item in itens_data:
            menu = session.get(Menu, item["menu_id"])
            cliente = session.get(Cliente, item["cliente_id"])
            if not menu:
                raise HTTPException(status_code=404, detail=f"Item do menu com ID {item['menu_id']} não encontrado")

            # Criar o objeto PedidoItem
            pedido_item = PedidoItem(
                cliente_id=cliente.id,
                pedido_id=pedido.id,
                menu_id=menu.id,
                quantidade=item["quantidade"]
            )
            session.add(pedido_item)

            # Calcular o total do pedido
            total += menu.preco * item["quantidade"]

        # Atualizar o total do pedido
        pedido.total = total
        session.commit()
        session.refresh(pedido)

        return {
            "id": pedido.id,
            "data": pedido.data,
            "total": pedido.total,
            "itens": [{"cliente_id": item["cliente_id"], "menu_id": item["menu_id"], "quantidade": item["quantidade"]} for item in itens_data]
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar pedido: {e}")

def listar_pedidos(session: Session, offset: int = 0, limit: int = Query(default=10, le=100)):
    try:
        with Session(engine) as session:
            statement = select(PedidoItem).offset(offset).limit(limit)
            pedido_itens = session.exec(statement).all()
            
            return [
                {
                    "id": item.id,
                    "pedido_id": item.pedido_id,
                    "cliente_id": item.cliente_id,
                    "menu_id": item.menu_id,
                    "quantidade": item.quantidade,
                    "total": item.menu.preco * item.quantidade if item.menu else None,
                    "menu_nome": item.menu.nome if item.menu else None,
                    "menu_preco": item.menu.preco if item.menu else None
                }
                for item in pedido_itens
            ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar pedidos: {e}")
    
def buscar_pedido(pedido_id: int, session: Session):
    try:
        with Session(engine) as session:
            statement = select(Pedido).where(Pedido.id == pedido_id)
            pedido = session.exec(statement).first()
            if not pedido:
                raise HTTPException(status_code=404, detail="Pedido não encontrado")
            return pedido
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar pedido: {e}")

def atualizar_pedido(pedido_id: int, pedido_data: dict, session: Session):
    try:
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
                session.query(Menu).filter(Menu.pedido_id == pedido_id).delete()
                # Adicionar os novos itens
                for item_data in pedido_data["itens"]:
                    item_data["pedido_id"] = pedido.id
                    pedido_item = Menu(**item_data)
                    session.add(pedido_item)
            
            session.commit()
            session.refresh(pedido)
        return pedido
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar pedido: {e}")

def remover_pedido(pedido_id: int, session: Session):
    try:
        with Session(engine) as session:
            # Excluir os itens associados ao pedido
            session.query(Menu).filter(Menu.pedido_id == pedido_id).delete()
            
            # Excluir o pedido
            statement = select(Pedido).where(Pedido.id == pedido_id)
            pedido = session.exec(statement).first()
            session.delete(pedido)
            session.commit()
            return pedido
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao remover pedido: {e}")