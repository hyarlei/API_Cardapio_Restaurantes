import csv
import os
from app.models.menu import MenuItem

MENU_FILE = "app/data/menu.csv"

def criar_menu_item(item: MenuItem):
    try:
        novo_id = 1
        if os.path.exists(MENU_FILE):
            with open(MENU_FILE, "r", newline='', encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile)
                next(reader, None)
                ids = [int(item[0]) for item in reader if item and item[0].isdigit()]
                novo_id = max(ids, default=0) + 1

        with open(MENU_FILE, "a", newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            
            if not os.path.exists(MENU_FILE) or os.stat(MENU_FILE).st_size == 0:
                writer.writerow(["id", "nome", "descricao", "preco", "tipo", "disponivel"])
            writer.writerow([novo_id, item.nome, item.descricao, item.preco, item.tipo, item.disponivel])
        return {"id": novo_id, "message": "Item criado com sucesso"}

    except Exception as e:
        raise RuntimeError(f"Erro ao criar item no menu: {e}")


def listar_menu_items():
    items = []
    try:
        if not os.path.exists(MENU_FILE) or os.stat(MENU_FILE).st_size == 0:
            return items

        with open(MENU_FILE, newline='', encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)
            for item in reader:
                if len(item) != 6:
                    continue
                items.append(MenuItem(
                    id=int(item[0]),
                    nome=item[1],
                    descricao=item[2],
                    preco=float(item[3]),
                    tipo=item[4],
                    disponivel=item[5].lower() == 'true'
                ))
    except FileNotFoundError:
        return items
    except Exception as e:
        raise RuntimeError(f"Erro ao listar itens do menu: {e}")
    return items
