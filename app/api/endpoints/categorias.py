from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import get_db 
from app.repositories import categoria_repo, producto_repo
from app.schemas.categoria_schema import CategoriaResponse
from app.schemas.producto_schema import ProductoResponse

router = APIRouter()

# Definimos el endpoint de tipo GET
@router.get("/buscar", response_model=CategoriaResponse)
def buscar_categoria_por_nombre(
    nombre: str, 
    db: Session = Depends(get_db)
):
    """
    Busca una categoría por su nombre exacto (insensible a mayúsculas).
    """
    categoria = categoria_repo.get_by_name(db, nombre_buscar=nombre)

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría '{nombre}' no encontrada"
        )
        
    return categoria

@router.get(
    "/buscar-por-categoria",
    response_model=list[ProductoResponse]
)
def buscar_productos_por_categoria(
    categoria: str,
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db)
):
    productos = producto_repo.consulta_por_categoria(
        db=db,
        nombre_categoria=categoria,
        page=page,
        size=size
    )

    if not productos:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron productos para la categoría '{categoria}'"
        )

    return productos