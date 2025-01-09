import sqlite3
from fastapi import HTTPException
from http import HTTPStatus
from app.models.menu import MenuItem
import hashlib
import zipfile
import os

DB_FILE = "app/data/menu.db"

# Inicializar o banco de dados (chamado no startup da aplicação)
def init_db():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS menu (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT NOT NULL,
                preco REAL NOT NULL,
                tipo TEXT NOT NULL,
                disponivel BOOLEAN NOT NULL
            )
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        raise RuntimeError(f"Erro ao inicializar o banco de dados: {e}")


def criar_menu_item(menu_item: MenuItem):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO menu (nome, descricao, preco, tipo, disponivel)
            VALUES (?, ?, ?, ?, ?)
        """, (menu_item.nome, menu_item.descricao, menu_item.preco, menu_item.tipo, menu_item.disponivel))
        conn.commit()

        menu_item.id = cursor.lastrowid
        conn.close()

        return {"id": menu_item.id, "message": "Item criado com sucesso"}
    except Exception as e:
        raise RuntimeError(f"Erro ao criar item do menu: {e}")


def listar_menu_items():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM menu")
        rows = cursor.fetchall()
        conn.close()

        items = [
            MenuItem(
                id=row[0],
                nome=row[1],
                descricao=row[2],
                preco=row[3],
                tipo=row[4],
                disponivel=row[5]
            )
            for row in rows
        ]
        return items
    except Exception as e:
        raise RuntimeError(f"Erro ao listar itens do menu: {e}")


def buscar_item_por_id(item_id: int):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM menu WHERE id = ?", (item_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Item não encontrado"
            )

        return MenuItem(
            id=row[0],
            nome=row[1],
            descricao=row[2],
            preco=row[3],
            tipo=row[4],
            disponivel=row[5]
        )
    except Exception as e:
        raise RuntimeError(f"Erro ao obter item do menu: {e}")


def atualizar_menu_item(item_id: int, item_atualizado: MenuItem):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM menu WHERE id = ?", (item_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Item não encontrado"
            )

        cursor.execute("""
            UPDATE menu
            SET nome = ?, descricao = ?, preco = ?, tipo = ?, disponivel = ?
            WHERE id = ?
        """, (item_atualizado.nome, item_atualizado.descricao, item_atualizado.preco, item_atualizado.tipo, item_atualizado.disponivel, item_id))
        conn.commit()
        conn.close()

        return {"message": "Item atualizado com sucesso"}
    except Exception as e:
        raise RuntimeError(f"Erro ao atualizar item do menu: {e}")


def remover_item(item_id: int):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM menu WHERE id = ?", (item_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Item não encontrado"
            )

        cursor.execute("DELETE FROM menu WHERE id = ?", (item_id,))
        conn.commit()
        conn.close()

        return {"message": "Item removido com sucesso"}
    except Exception as e:
        raise RuntimeError(f"Erro ao remover item do menu: {e}")


def contar_itens_menu():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM menu")
        count = cursor.fetchone()[0]
        conn.close()

        return {"quantidade_itens": count}
    except Exception as e:
        raise RuntimeError(f"Erro ao contar itens do menu: {e}")


def obter_menu_hash():
    try:
        sha256_hash = hashlib.sha256()
        with open(DB_FILE, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return {"hash": sha256_hash.hexdigest()}
    except Exception as e:
        raise RuntimeError(f"Erro ao calcular hash do menu: {e}")


def compactar_db():
    try:
        with zipfile.ZipFile("app/data/menu.zip", "w") as zip:
            zip.write(DB_FILE, os.path.basename(DB_FILE))
        return {"message": "Banco de dados compactado com sucesso"}
    except Exception as e:
        raise RuntimeError(f"Erro ao compactar banco de dados: {e}")
