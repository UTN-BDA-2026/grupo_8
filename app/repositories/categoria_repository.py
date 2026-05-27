from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from app.models import Categoria

class CategoriaRepository:
    def get_by_name(self, db: Session, nombre_buscar: str) -> List[Categoria]:
        # Usamos ilike de Postgres para que busque "electronica" o "Electronica" por igual
        query = select(Categoria).where(Categoria.nombre.ilike(f"%{nombre_buscar}%"))
        result = db.execute(query)
        return result.scalars().all()

categoria_repo = CategoriaRepository()