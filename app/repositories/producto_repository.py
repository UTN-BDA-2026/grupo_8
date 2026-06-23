from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, or_, text, func
from typing import List, Optional
from app.models import Producto, Ranking
from sqlalchemy import case
from app.db.redis import get_redis

import logging
import time
import json 
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
        
        import redis
        from app.db.redis import pool
        
        try:
            redis_client = redis.Redis(connection_pool=pool)
        except Exception as e:
            logger.error(f"⚠️ No se pudo inicializar Redis en el repositorio: {e}")
            redis_client = None

        cache_key = f"busqueda:{texto_limpio.lower()}:limit_{limit}"

        # Intentar leer de la caché de Redis antes de tocar Postgres
        if redis_client:
            try:
                cached_data = redis_client.get(cache_key)
                if cached_data:
                    logger.info(f"⚡ [Redis] Hit de caché para la clave: {cache_key}")
                    logger.info(f"Tiempo total busqueda_unificada (Caché): {time.perf_counter() - inicio_total:.4f} segundos")
                    return json.loads(cached_data)
            except Exception as e:
                logger.error(f"⚠️ Error al leer de Redis: {e}")

        # Función auxiliar para mapear las filas de Postgres a diccionarios
        def map_result(rows):
            return [
                {
                    "id_producto": r.id_producto,
                    "asin": r.asin,
                    "titulo": r.titulo,
                    "marca": r.marca,
                    "descripcion": r.descripcion,
                    "precio": float(r.precio) if r.precio else None,
                    "fecha_publicacion": str(r.fecha_publicacion) if r.fecha_publicacion else None,
                    "categoria_principal": None,
                    "posicion": None,
                    "imagenes": [img.url for img in r.imagenes]  
                }
                for r in rows
            ]

        # Variable para guardar los resultados de Postgres si los encontramos
        resultado_final = None

        # Exact match
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
            resultado_final = map_result(exactos)

        # Full-text search (Si no hubo exact match)
        if not resultado_final:
            inicio = time.perf_counter()
            query_fts = func.plainto_tsquery("english", texto_limpio)
            fts = (
                db.query(Producto)
                .options(joinedload(Producto.imagenes))  
                .filter(Producto.search_vector.op("@@")(query_fts))
                .order_by(func.ts_rank(Producto.search_vector, query_fts).desc())
                .limit(limit)
                .all()
            )
            logger.info(f"FTS ejecutado en {time.perf_counter() - inicio:.4f} segundos")
            if fts:
                resultado_final = map_result(fts)

        # Trigram similarity (Si no hubo FTS)
        if not resultado_final:
            inicio = time.perf_counter()
            trigram = (
                db.query(Producto)
                .options(joinedload(Producto.imagenes))  
                .filter(Producto.titulo.op("%")(texto_limpio))
                .order_by(func.similarity(Producto.titulo, texto_limpio).desc())
                .limit(limit)
                .all()
            )
            logger.info(f"Trigram ejecutado en {time.perf_counter() - inicio:.4f} segundos")
            resultado_final = map_result(trigram)

        # Guardar en Redis si encontramos resultados
        if redis_client and resultado_final:
            try:
                redis_client.setex(cache_key, 300, json.dumps(resultado_final))
                logger.info(f"💾 [Redis] Resultados guardados en caché para: {cache_key}")
            except Exception as e:
                logger.error(f"⚠️ Error al guardar en Redis: {e}")

        logger.info(f"Tiempo total busqueda_unificada (Postgres): {time.perf_counter() - inicio_total:.4f} segundos")
        
        return resultado_final
    
producto_repo = ProductoRepository()