import logging
import os
import redis

logger = logging.getLogger("app.db.redis_client")
logging.basicConfig(level=logging.INFO)

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

logger.info(f"Inicializando pool de Redis apuntando a {REDIS_HOST}:{REDIS_PORT}...")

pool = redis.ConnectionPool(
    host=REDIS_HOST, 
    port=REDIS_PORT, 
    password=REDIS_PASSWORD, 
    decode_responses=True
)

def get_redis():
    client = redis.Redis(connection_pool=pool)
    try:
        client.ping()
        logger.info("Conexión exitosa a Redis (Ping OK)")
        yield client
    except redis.exceptions.AuthenticationError:
        logger.error("Error de autenticación en Redis: Verifica la contraseña en el .env")
        yield None
    except redis.exceptions.ConnectionError as e:
        logger.warning(f"Redis no está disponible (Modo offline). Detalle: {e}")
        yield None
    finally:
        client.close()
        