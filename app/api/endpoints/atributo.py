from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db 
from app.models.atributos import Atributo
from app.repositories import atributo_repo  
from app.schemas.atributo_schema import AtributoCreate, AtributoResponse

router = APIRouter()


@router.get("/producto/{id_producto}", response_model=List[AtributoResponse])
def buscar_atributos_por_producto(
    id_producto: int, 
    db: Session = Depends(get_db)
):
    """
    Trae todos los atributos que le pertenecen a un mismo producto.
    """
    atributos = atributo_repo.buscar_por_producto(db, id_producto=id_producto)
    return atributos


@router.get("/buscar", response_model=List[AtributoResponse])
def buscar_atributos_por_clave(
    clave: str, 
    db: Session = Depends(get_db)
):
    """
    Busca atributos por coincidencia parcial en la clave (ej: 'color').
    """
    atributos = atributo_repo.buscar_por_clave(db, clave=clave)
    
    if not atributos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron atributos con la clave '{clave}'"
        )
        
    return atributos