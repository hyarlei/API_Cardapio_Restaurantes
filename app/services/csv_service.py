import os, zipfile
import pandas as pd
from app.models.menu import MenuItem
from fastapi import HTTPException
from http import HTTPStatus

MENU_FILE = "app/data/menu.csv"

def criar_menu_item(menu_item: MenuItem):
    try:
        id = 0

        if os.path.exists(MENU_FILE) and os.path.getsize(MENU_FILE) > 0:
            try:
                df = pd.read_csv(MENU_FILE, index_col=False)
                if not df.empty and "id" in df.columns:
                    id = int(df["id"].max() + 1)
            except pd.errors.EmptyDataError:
                df = pd.DataFrame()
        else:
            df = pd.DataFrame()

        menu_item.id = id
        novo_item_df = pd.DataFrame([menu_item.model_dump()])

        if not os.path.exists(MENU_FILE) or os.path.getsize(MENU_FILE) == 0:
            os.makedirs(os.path.dirname(MENU_FILE), exist_ok=True)
            novo_item_df.to_csv(MENU_FILE, index=False, header=True)
        else:
            novo_item_df.to_csv(MENU_FILE, mode='a', index=False, header=False)

        return {"id": menu_item.id, "message": "Item criado com sucesso"}

    except Exception as e:
        raise RuntimeError(f"Erro ao criar item do menu: {e}")

def listar_menu_items():
    try:
        if not os.path.exists(MENU_FILE) or os.stat(MENU_FILE).st_size == 0:
            return []

        df = pd.read_csv(MENU_FILE)
        items = []
        for _, item in df.iterrows():
            items.append(MenuItem(id=int(item["id"]), nome=item["nome"], descricao=item["descricao"], preco=float(item["preco"]), tipo=item["tipo"], disponivel=item["disponivel"]))

        return items
    except Exception as e:
        raise RuntimeError(f"Erro ao listar itens do menu: {e}")
    
def atualizar_menu_item(item_id: int, item_atualizado: MenuItem):
    try:
        if not os.path.exists(MENU_FILE) or os.stat(MENU_FILE).st_size == 0:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Menu vazio")
        
        df = pd.read_csv(MENU_FILE)
        item = df.loc[df["id"] == item_id]
        if item.empty:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Item não encontrado")
        
        item_atualizado.id = item_id
        df.loc[df["id"] == item_id] = list(item_atualizado.model_dump().values())
        df.to_csv(MENU_FILE, index=False)
        return {"message": "Item atualizado com sucesso"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise RuntimeError(f"Erro ao atualizar item do menu: {e}")
    
def remover_menu_item(item_id: int):
    try:
        if not os.path.exists(MENU_FILE) or os.stat(MENU_FILE).st_size == 0:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Menu vazio")
        
        df = pd.read_csv(MENU_FILE)
        item = df.loc[df["id"] == item_id]
        if item.empty:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Item não encontrado")
        
        df = df.drop(df[df["id"] == item_id].index)
        df.to_csv(MENU_FILE, index=False)
        return {"message": "Item removido com sucesso"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise RuntimeError(f"Erro ao remover item do menu: {e}")
    
def compactar_csv():
    try:
        with zipfile.ZipFile("app/data/menu.zip", "w") as zip:
            zip.write(MENU_FILE, os.path.basename(MENU_FILE))
        return {"message": "CSV compactado com sucesso"}
    except Exception as e:
        raise RuntimeError(f"Erro ao compactar CSV: {e}")