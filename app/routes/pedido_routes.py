from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session
from app.db import get_session
from app.services.pedido_service import (
    criar_pedido,
    listar_pedidos,
    buscar_pedido,
    atualizar_pedido,
    remover_pedido
)

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_pedido(pedido_data: dict, session: Session = Depends(get_session)):
    criar_pedido(session, pedido_data)
    return {"message": "Pedido criado com sucesso"}

@router.get("/{pedido_id}", status_code=status.HTTP_200_OK)
async def read_pedido(pedido_id: int, session: Session = Depends(get_session)):
    pedido = buscar_pedido(pedido_id, session)
    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido

@router.get("/", status_code=status.HTTP_200_OK)
async def read_pedidos(session: Session = Depends(get_session)):
    return listar_pedidos(session)

@router.put("/{pedido_id}", status_code=status.HTTP_200_OK)
async def update_pedido(pedido_id: int, pedido_data: dict, session: Session = Depends(get_session)):
    pedido = atualizar_pedido(pedido_id, pedido_data, session)
    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return {"message": "Pedido atualizado com sucesso"}

@router.delete("/{pedido_id}", status_code=status.HTTP_200_OK)
async def delete_pedido(pedido_id: int, session: Session = Depends(get_session)):
    pedido = remover_pedido(pedido_id, session)
    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return {"message": "Pedido removido com sucesso"}