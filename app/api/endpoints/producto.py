from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
import time
import logging

from app.db.session import get_db
from app.repositories import producto_repo
from app.schemas.producto_schema import ProductoResponse

router = APIRouter()
logger = logging.getLogger("app.api.endpoints.producto")

@router.get("/buscar", response_model=List[ProductoResponse])
def buscar_productos_avanzado(
    titulo: str = Query(..., description="Texto a buscar"),
    limit: int = Query(20, ge=1, le=100, description="Cantidad máxima de resultados"),
    db: Session = Depends(get_db)
):
    if not titulo.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe ingresar un término de búsqueda válido."
        )

    inicio = time.perf_counter()
    productos = producto_repo.busqueda_unificada(db, texto=titulo, limit=limit)
    logger.info(f"Tiempo total busqueda_unificada (endpoint): {time.perf_counter() - inicio:.4f} segundos")

    if not productos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron productos para '{titulo}'"
        )

    return productos


@router.get("/{asin}", response_model=ProductoResponse)
def obtener_producto_por_asin(asin: str, db: Session = Depends(get_db)):
    inicio = time.perf_counter()
    producto = producto_repo.obtener_por_asin(db, asin=asin)
    logger.info(f"Tiempo obtener_por_asin (endpoint): {time.perf_counter() - inicio:.4f} segundos")

    if producto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe un producto con ASIN '{asin}'"
        )
    return producto

