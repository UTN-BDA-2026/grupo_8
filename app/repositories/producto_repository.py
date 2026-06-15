from sqlalchemy.orm import Session
from sqlalchemy import select, or_, text, func
from typing import List, Optional
from app.models import Producto, Ranking

class ProductoRepository:

    def obtener_por_asin(self, db: Session, asin: str) -> Optional[Producto]:
        """Busca un producto por su código ASIN único (Pantalla de detalle)"""
        consulta = select(Producto).where(Producto.asin == asin)
        return db.execute(consulta).scalar_one_or_none()

    def consulta_por_categoria(self, db: Session, nombre_categoria: str, page: int = 1, size: int = 10):
        """Lista productos de una categoría ordenados por popularidad (Navegación por menú)"""
        consulta = (select(Producto).join(Ranking, Producto.id_producto == Ranking.id_producto)
            .where(Ranking.categoria == nombre_categoria)
            .order_by(Ranking.posicion)
            .offset((page - 1) * size)
            .limit(size))
        resultado = db.execute(consulta)
        return resultado.scalars().all()

    def busqueda_unificada(self, db: Session, texto: str, limit: int = 20) -> List[Producto]:
        """
        El cerebro del buscador: procesa el texto de la barra única.
        Busca por coincidencia exacta, palabras sueltas (FTS) y errores ortográficos.
        Alinea todo según la popularidad del Ranking de Amazon.
        """
        texto_limpio = texto.strip()
        if not texto_limpio:
            return []

        query_fts = " & ".join(texto_limpio.split())

        condiciones = or_(
            Producto.titulo.ilike(texto_limpio),
            Producto.search_vector.op('@@')(func.to_tsquery('spanish', query_fts)),
            Producto.titulo.op("%")(texto_limpio)
        )

        consulta = (
            select(Producto)
            .outerjoin(Ranking, Producto.id_producto == Ranking.id_producto)
            .where(condiciones)
        )

        orden_exacto = text(f"CASE WHEN LOWER(productos.titulo) = LOWER('{texto_limpio}') THEN 1 ELSE 0 END DESC")
        orden_fts = func.ts_rank(Producto.search_vector, func.to_tsquery('spanish', query_fts)).desc()
        orden_trigramas = text(f"similarity(productos.titulo, '{texto_limpio}') DESC")
        orden_ranking = text("COALESCE(ranking.posicion, 999999) ASC")
        

        consulta = consulta.order_by(
            orden_exacto,
            orden_fts,
            orden_trigramas,
            orden_ranking
        ).limit(limit)

        resultado = db.execute(consulta)
        return resultado.scalars().all()

producto_repo = ProductoRepository()