from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, or_, text, func
from typing import List, Optional
from app.models import Producto, Ranking
from sqlalchemy import case

import logging
import time

logger = logging.getLogger(__name__)



class ProductoRepository:

    def obtener_por_asin(self, db: Session, asin: str) -> Optional[Producto]:
        """Busca un producto por su código ASIN único (Pantalla de detalle)"""
        consulta = select(Producto).where(Producto.asin == asin)
        return db.execute(consulta).scalar_one_or_none()

    def consulta_por_categoria(self, db: Session, id_categoria: int, page: int = 1, size: int = 10):
        productos = (
            db.query(Producto)
            .options(joinedload(Producto.imagenes))  # 🔴 eager load imágenes
            .join(Ranking, Producto.id_producto == Ranking.id_producto)
            .filter(Ranking.id_categoria == id_categoria)
            .order_by(Ranking.posicion.asc())
            .offset((page - 1) * size)
            .limit(size)
            .all()
        )

        # Mapear resultados a dict con imágenes
        resultado = [
            {
                "id_producto": p.id_producto,
                "asin": p.asin,
                "titulo": p.titulo,
                "marca": p.marca,
                "descripcion": p.descripcion,
                "precio": float(p.precio) if p.precio else None,
                "fecha_publicacion": p.fecha_publicacion,
                "posicion": p.ranking.posicion if p.ranking else None,
                "imagenes": [img.url for img in p.imagenes]  # 🔴 ya están cargadas
            }
            for p in productos
        ]

        return resultado

    def busqueda_unificada(self, db: Session, texto: str, limit: int = 20):
        inicio_total = time.perf_counter()
        texto_limpio = texto.strip()
        if not texto_limpio:
            return []

        def map_result(rows):
            return [
                {
                    "id_producto": r.id_producto,
                    "asin": r.asin,
                    "titulo": r.titulo,
                    "marca": r.marca,
                    "descripcion": r.descripcion,
                    "precio": float(r.precio) if r.precio else None,
                    "fecha_publicacion": r.fecha_publicacion,
                    "categoria_principal": None,
                    "posicion": None,
                    "imagenes": [img.url for img in r.imagenes]  
                }
                for r in rows
            ]

        # 1. Exact match
        inicio = time.perf_counter()
        exactos = (
            db.query(Producto)
            .options(joinedload(Producto.imagenes))  
            .filter(func.lower(Producto.titulo) == texto_limpio.lower())
            .limit(limit)
            .all()
        )
        logger.info(f"Exact match ejecutado en {time.perf_counter() - inicio:.4f} segundos")
        if exactos:
            logger.info(f"Tiempo total busqueda_unificada: {time.perf_counter() - inicio_total:.4f} segundos")
            return map_result(exactos)

        # 2. Full-text search
        inicio = time.perf_counter()
        query_fts = func.plainto_tsquery("english", texto_limpio)
        fts = (
            db.query(Producto)
            .options(joinedload(Producto.imagenes))  # 🔴 eager load
            .filter(Producto.search_vector.op("@@")(query_fts))
            .order_by(func.ts_rank(Producto.search_vector, query_fts).desc())
            .limit(limit)
            .all()
        )
        logger.info(f"FTS ejecutado en {time.perf_counter() - inicio:.4f} segundos")
        if fts:
            logger.info(f"Tiempo total busqueda_unificada: {time.perf_counter() - inicio_total:.4f} segundos")
            return map_result(fts)

        # 3. Trigram similarity
        inicio = time.perf_counter()
        trigram = (
            db.query(Producto)
            .options(joinedload(Producto.imagenes))  # 🔴 eager load
            .filter(Producto.titulo.op("%")(texto_limpio))
            .order_by(func.similarity(Producto.titulo, texto_limpio).desc())
            .limit(limit)
            .all()
        )
        logger.info(f"Trigram ejecutado en {time.perf_counter() - inicio:.4f} segundos")
        logger.info(f"Tiempo total busqueda_unificada: {time.perf_counter() - inicio_total:.4f} segundos")
        return map_result(trigram)
    
producto_repo = ProductoRepository()