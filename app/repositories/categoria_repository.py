from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional
from app.models import Categoria

class CategoriaRepository:
    def get_by_name(self, db: Session, nombre_buscar: str) -> Optional[Categoria]:
        query = select(Categoria).where(Categoria.nombre.ilike(nombre_buscar))
        result = db.execute(query)
        return result.scalar()

categoria_repo = CategoriaRepository()