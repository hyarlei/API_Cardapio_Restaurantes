from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models.modelagem import Cliente, Menu, Pedido
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "API_Cardapio_Restaurante"

client = AsyncIOMotorClient(MONGO_URI)
db = client.get_database(DB_NAME)

async def init_db():
    await init_beanie(database=db, document_models=[Cliente, Menu, Pedido])
    print("Banco de dados conectado com sucesso!")