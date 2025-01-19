from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.menu import Menu, TipoMenu
from app.db import engine
from datetime import datetime

def criar_menu_item(session: Session, menu_item: dict):
    try:
        with Session(engine) as session:
            # Verificar se o tipo é válido
            if menu_item.get("tipo") not in TipoMenu.__members__:
                raise HTTPException(status_code=400, detail=f"Tipo inválido: {menu_item.get('tipo')}")
            
            # Converter a string data em um objeto datetime
            if "data" in menu_item:
                menu_item["data"] = datetime.fromisoformat(menu_item["data"])
            
            menu_item = Menu(**menu_item)
            session.add(menu_item)
            session.commit()
            session.refresh(menu_item)
            return menu_item
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar item no menu: {e}")

def listar_menu_items(session: Session, offset: int = 0, ano: int = None, titulo: str = None, tipo: str = None, limit: int = 100, order_by: str = "id"):
    try:
        with Session(engine) as session:
            statement = select(Menu).offset(offset).limit(limit)
            if tipo:
                statement = statement.where(Menu.tipo == tipo)
            if ano:
                statement = statement.where(Menu.data.between(f"{ano}-01-01", f"{ano}-12-31"))
            if titulo:
                statement = statement.where(Menu.nome.contains(titulo))
            if order_by:
                statement = statement.order_by(getattr(Menu, order_by))
            menu_items = session.exec(statement).all()
            return menu_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar itens do menu: {e}")

def buscar_menu_item(menu_id: int, session: Session):
    try:
        with Session(engine) as session:
            menu_item = session.get(Menu, menu_id)
            if not menu_item:
                raise HTTPException(status_code=404, detail="Item do menu não encontrado")
            return menu_item
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar item do menu: {e}")

def atualizar_menu_item(menu_id: int, menu_data: dict, session: Session):
    try:
        with Session(engine) as session:
            menu_item = session.get(Menu, menu_id)
            if not menu_item:
                raise HTTPException(status_code=404, detail="Item do menu não encontrado")
            
            # Verificar se o tipo é válido
            if "tipo" in menu_data and menu_data["tipo"] not in TipoMenu.__members__:
                raise HTTPException(status_code=400, detail=f"Tipo inválido: {menu_data['tipo']}")
            
            for key, value in menu_data.items():
                setattr(menu_item, key, value)
            session.add(menu_item)
            session.commit()
            session.refresh(menu_item)
            return menu_item
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar item do menu: {e}")

def remover_menu_item(menu_id: int, session: Session):
    try:
        with Session(engine) as session:
            menu_item = session.get(Menu, menu_id)
            if not menu_item:
                raise HTTPException(status_code=404, detail="Item do menu não encontrado")
            session.delete(menu_item)
            session.commit()
            return menu_item
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao remover item do menu: {e}")