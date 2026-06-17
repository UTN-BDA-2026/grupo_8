from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional
from app.models import Producto
from typing import List
from app.models import Producto, Ranking

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
    

    def consulta_por_categoria2(self, db: Session, id_categoria: int, page: int = 1, size: int = 10):
        return (
            db.query(Producto)
            .join(Ranking, Producto.id_producto == Ranking.id_producto)
            .filter(Ranking.id_categoria == id_categoria)
            .order_by(Ranking.posicion.asc())
            .offset((page - 1) * size)
            .limit(size)
            .all()
        )
    def consulta_por_categoria(self, db: Session, id_categoria: int, page: int = 1, size: int = 10):
        return (
            db.query(
                Producto.id_producto,
                Producto.asin,
                Producto.titulo,
                Producto.marca,
                Producto.descripcion,
                Producto.precio,
                Producto.fecha_publicacion,
                Ranking.posicion.label("posicion")   # 👈 incluir ranking
            )
            .join(Ranking, Producto.id_producto == Ranking.id_producto)
            .filter(Ranking.id_categoria == id_categoria)
            .order_by(Ranking.posicion.asc())
            .offset((page - 1) * size)
            .limit(size)
            .all()
        )


producto_repo = ProductoRepository()
