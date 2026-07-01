from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional
from app.db.redis import pool
import redis
import logging
import time
import json

logger = logging.getLogger(__name__)

from app.models import Categoria

class CategoriaRepository:

    def get_by_name(self, db: Session, nombre_buscar: str) -> Optional[dict]:
        inicio_total = time.perf_counter()
        nombre_limpio = nombre_buscar.strip()
        
        if not nombre_limpio:
            return None
        
        try:
            redis_client = redis.Redis(connection_pool=pool)
        except Exception as e:
            logger.error(f"⚠️ No se pudo inicializar Redis en el repositorio: {e}")
            redis_client = None

        cache_key = f"categoria_nombre:{nombre_limpio.lower()}"

        if redis_client:
            try:
                cached_data = redis_client.get(cache_key)
                if cached_data:
                    logger.info(f"⚡ [Redis] Hit de caché para la clave: {cache_key}")
                    logger.info(f"Tiempo total get_by_name (Caché): {time.perf_counter() - inicio_total:.4f} segundos")
                    return json.loads(cached_data)
            except Exception as e:
                logger.error(f"⚠️ Error al leer de Redis: {e}")

        # Función auxiliar para mapear el objeto de Postgres a diccionario 
        def map_result(c):
            return {
                "id_categoria": c.id_categoria,
                "nombre": c.nombre,
                
            }

        #  No hubo hit de caché -> Vamos a Postgres
        inicio = time.perf_counter()
        query = select(Categoria).where(Categoria.nombre.ilike(nombre_limpio))
        result = db.execute(query)
        categoria = result.scalar()
        logger.info(f"Consulta get_by_name ejecutada en {time.perf_counter() - inicio:.4f} segundos")

        if not categoria:
            logger.info(f"Tiempo total get_by_name (Postgres, sin resultado): {time.perf_counter() - inicio_total:.4f} segundos")
            return None

    
        resultado_final = map_result(categoria)

        #  Guardar en Redis
        if redis_client:
            try:
                redis_client.setex(cache_key, 300, json.dumps(resultado_final))
                logger.info(f"💾 [Redis] Resultado guardado en caché para: {cache_key}")
            except Exception as e:
                logger.error(f"⚠️ Error al guardar en Redis: {e}")

        logger.info(f"Tiempo total get_by_name (Postgres): {time.perf_counter() - inicio_total:.4f} segundos")

        return resultado_final

categoria_repo = CategoriaRepository()