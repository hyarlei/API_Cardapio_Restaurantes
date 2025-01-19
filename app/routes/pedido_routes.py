from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from datetime import datetime
from app.db import get_session
from app.services.pedido_service import (
    criar_pedido,
    listar_pedidos,
    buscar_pedido,
    atualizar_pedido,
    remover_pedido
)
from app.models.pedido import Pedido

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_pedido(pedido_data: dict, session: Session = Depends(get_session)):
    pedido = criar_pedido(session, pedido_data)
    return pedido

@router.get("/{pedido_id}", status_code=status.HTTP_200_OK)
def read_pedido(pedido_id: int, session: Session = Depends(get_session)):
    pedido = buscar_pedido(session, pedido_id)
    return pedido

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Pedido])
def read_pedidos(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    ano: int = Query(None, ge=1900, le=datetime.now().year),
    order_by: str = Query("id"),
    session: Session = Depends(get_session)
):
    return listar_pedidos(session, offset=offset, limit=limit, ano=ano, order_by=order_by)

@router.put("/{pedido_id}", status_code=status.HTTP_200_OK)
def update_pedido(pedido_id: int, pedido_data: dict, session: Session = Depends(get_session)):
    atualizar_pedido(pedido_id, pedido_data,session)
    return {Pedido}

@router.delete("/{pedido_id}", status_code=status.HTTP_200_OK)
def delete_pedido(pedido_id: int, session: Session = Depends(get_session)):
    remover_pedido(pedido_id,session)
    return {"message": "Pedido removido com sucesso"}
