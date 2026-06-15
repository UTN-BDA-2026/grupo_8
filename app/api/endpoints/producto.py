from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.repositories import producto_repo
from app.schemas.producto_schema import ProductoResponse

router = APIRouter()


@router.get("/buscar", response_model=List[ProductoResponse])
def buscar_productos_por_titulo(
    titulo: str,
    db: Session = Depends(get_db)
):
    """
    Busca productos por coincidencia parcial en el título.
    """
    return producto_repo.buscar_por_titulo(db, titulo_buscar=titulo)

@router.get("/buscar-palabras", response_model=List[ProductoResponse])
def buscar_productos_por_palabras(texto: str, db: Session = Depends(get_db)):
    """
    Busca productos que contengan todas las palabras indicadas en el título.
    """
    productos = producto_repo.buscar_por_palabras(db, texto)

    if not productos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron productos para '{texto}'"
        )

    return productos

@router.get("/buscar-descripcion", response_model=List[ProductoResponse])
def buscar_productos_por_descripcion(
    texto: str,
    db: Session = Depends(get_db)
):
    """
    Busca productos cuya descripción contenga el texto indicado.
    """

    productos = producto_repo.buscar_por_descripcion(
        db,
        texto
    )

    if not productos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron productos con '{texto}' en la descripción"
        )

    return productos

@router.get("/{asin}", response_model=ProductoResponse)
def obtener_producto_por_asin(asin: str, db: Session = Depends(get_db)):
    """
    Obtiene un producto a partir de su ASIN.
    """
    producto = producto_repo.obtener_por_asin(db, asin=asin)

    if producto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe un producto con ASIN '{asin}'"
        )

    return producto

