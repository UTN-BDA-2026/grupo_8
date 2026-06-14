from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional
from app.models import Producto

class ProductoRepository:
    def buscar_por_titulo(self, db: Session, titulo_buscar: str) -> List[Producto]:
        # Usamos ilike de Postgres para que busque "electronica" o "Electronica" por igual
        consulta = select(Producto).where(Producto.titulo.ilike(f"%{titulo_buscar}%"))
        resultado = db.execute(consulta)
        return resultado.scalars().all()

    def obtener_por_asin(self, db: Session, asin: str) -> Optional[Producto]:
        """Busca un producto por su código ASIN de Amazon"""
        consulta = select(Producto).where(Producto.asin == asin)
        return db.execute(consulta).scalar_one_or_none()
    
producto_repo = ProductoRepository()