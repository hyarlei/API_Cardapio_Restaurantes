from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session
from app.db import get_session
from app.services.cliente_service import (
    criar_cliente,
    listar_clientes,
    buscar_cliente,
    atualizar_cliente,
    remover_cliente
)

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_cliente(cliente_data: dict, session: Session = Depends(get_session)):
    criar_cliente(session, cliente_data)
    return {"message": "Cliente adicionado com sucesso"}

@router.get("/{cliente_id}", status_code=status.HTTP_200_OK)
async def read_cliente(cliente_id: int, session: Session = Depends(get_session)):
    cliente = buscar_cliente(cliente_id, session)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

@router.get("/", status_code=status.HTTP_200_OK)
async def read_clientes(session: Session = Depends(get_session)):
    return listar_clientes(session)

@router.put("/{cliente_id}", status_code=status.HTTP_200_OK)
async def update_cliente(cliente_id: int, cliente_data: dict, session: Session = Depends(get_session)):
    cliente = atualizar_cliente(cliente_id, cliente_data, session)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return {"message": "Cliente atualizado com sucesso"}

@router.delete("/{cliente_id}", status_code=status.HTTP_200_OK)
async def delete_cliente(cliente_id: int, session: Session = Depends(get_session)):
    cliente = remover_cliente(cliente_id, session)
    if cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return {"message": "Cliente removido com sucesso"}