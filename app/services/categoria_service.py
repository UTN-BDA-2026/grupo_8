from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List
from app.repositories import categoria_repo
from app.models.categoria import Categoria

class CategoriaService:
    def buscar_por_nombre(self, db: Session, nombre: str) -> List[Categoria]:
        # Validaciones de negocio si hicieran falta (ej: que el término no sea vacío)
        if not nombre.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El término de búsqueda no puede estar vacío."
            )
            
        categorias = categoria_repo.get_by_name(db, nombre_buscar=nombre)
        
        # Opcional: Podrías lanzar un 404 si querés, o simplemente devolver la lista vacía []
        if not categorias:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No se encontraron categorías que coincidan con '{nombre}'"
            )
            
        return categorias

# Instancia lista para importar
categoria_service = CategoriaService()