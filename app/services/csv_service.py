import csv
from app.models.menu import MenuItem

MENU_FILE = "app/data/menu.csv"

# MenuItem
def criar_menu_item(item: MenuItem):
    with open(MENU_FILE, "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([str(item.nome), str(item.descricao), str(item.preco), str(item.tipo), str(item.disponivel)])

def listar_menu_items():
    items = []
    with open(MENU_FILE, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            items.append(MenuItem(nome=row[0], descricao=row[1], preco=float(row[2]), tipo=row[3], disponivel=row[4] == 'True'))
    return items