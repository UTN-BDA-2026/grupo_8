from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from app.models import Producto

class ProductoRepository:
    def consulta_por_nombre(self, db: Session, nombre_buscar: str) -> List[Producto]:
        # Usamos ilike de Postgres para que busque "electronica" o "Electronica" por igual
        consulta = select(Producto).where(Producto.titulo.ilike(f"%{nombre_buscar}%"))
        resultado = db.execute(consulta)
        return resultado.scalars().all()

producto_repo = ProductoRepository()