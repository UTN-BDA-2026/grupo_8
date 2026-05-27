from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from app.models import Categoria

class CategoriaRepository:
    def buscar_por_nombre(self, db: Session, nombre_buscar: str) -> List[Categoria]:
        # Usamos ilike de Postgres para que busque "electronica" o "Electronica" por igual
        consulta = select(Categoria).where(Categoria.nombre.ilike(f"%{nombre_buscar}%"))
        resultado = db.execute(consulta)
        return resultado.scalars().all()

categoria_repo = CategoriaRepository()