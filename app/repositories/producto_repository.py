from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from app.models import Producto, Ranking

class ProductoRepository:
    def consulta_por_nombre(self, db: Session, nombre_buscar: str) -> List[Producto]:
        # Usamos ilike de Postgres para que busque "electronica" o "Electronica" por igual
        consulta = select(Producto).where(Producto.titulo.ilike(f"%{nombre_buscar}%"))
        resultado = db.execute(consulta)
        return resultado.scalars().all()

    def obtener_por_asin(self, db: Session, asin: str) -> Optional[Producto]:
        """Busca un producto por su código ASIN de Amazon"""
        consulta = select(Producto).where(Producto.asin == asin)
        return db.execute(consulta).scalar_one_or_none()
    

    def consulta_por_categoria(self, db: Session, nombre_categoria: str, page: int = 1, size: int = 10):
        consulta = (select(Producto).join(Ranking, Producto.id_producto == Ranking.id_producto)
            .where(Ranking.categoria == nombre_categoria)
            .order_by(Ranking.posicion)
            .offset((page - 1) * size)
            .limit(size))

        resultado = db.execute(consulta)
        return resultado.scalars().all()

producto_repo = ProductoRepository()
