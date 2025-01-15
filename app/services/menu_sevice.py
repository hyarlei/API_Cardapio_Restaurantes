from sqlmodel import SQLModel, Session, select
from app.models.menu import Menu
from app.db import engine

def init_db():
    SQLModel.metadata.create_all(engine)

def criar_menu_item(session: Session, menu_item: dict):
    with Session(engine) as session:
        menu_item = Menu(**menu_item)
        session.add(menu_item)
        session.commit()
        session.refresh(menu_item)
    return menu_item

def listar_menu_items(session: Session):
    with Session(engine) as session:
        statement = select(Menu)
        return session.exec(statement).all()

def buscar_menu_item(menu_item_id: int, session: Session):
    with Session(engine) as session:
        statement = select(Menu).where(Menu.id == menu_item_id)
        return session.exec(statement).first()

def atualizar_menu_item(menu_item_id: int, menu_item: dict, session: Session):
    with Session(engine) as session:
        statement = select(Menu).where(Menu.id == menu_item_id)
        menu = session.exec(statement).first()
        for key, value in menu_item.items():
            setattr(menu, key, value)
        session.add(menu)
        session.commit()
        session.refresh(menu)
    return menu

def remover_menu_item(menu_item_id: int, session: Session):
    with Session(engine) as session:
        statement = select(Menu).where(Menu.id == menu_item_id)
        menu = session.exec(statement).first()
        session.delete(menu)
        session.commit()
        return menu

def contar_menu_items(session: Session):
    with Session(engine) as session:
        statement = select(Menu)
        return session.exec(statement).count()