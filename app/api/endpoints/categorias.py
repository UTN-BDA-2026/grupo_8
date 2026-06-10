from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import get_db 
from app.repositories import categoria_repo
from app.schemas.categoria_schema import CategoriaResponse

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