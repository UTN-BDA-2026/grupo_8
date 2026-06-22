from fastapi import FastAPI, Depends
from app.db.session import get_db, engine
from sqlalchemy.orm import Session
from app.db.base_class import Base
from app.api.endpoints.categorias import router as categorias_router
from app.api.endpoints.atributo import router as atributos_router
from app.api.endpoints.producto import router as productos_router
from app.db.redis import get_redis
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(title="Buscador de Productos con FastAPI")

app.include_router(categorias_router, prefix="/categorias", tags=["Categorías"])
app.include_router(atributos_router, prefix="/atributos", tags=["Atributos"])
app.include_router(productos_router, prefix="/productos", tags=["Productos"])


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

@app.get("/")
def home():
    return {"message": "API del buscador levantada correctamente"}

@app.get("/test-db")
def probar_conexion(db: Session = Depends(get_db)):
    return {"status": "Conectado a la base de datos exitosamente", "database": str(db)}

@app.get("/test-redis", tags=["default"])

def test_redis(redis = Depends(get_redis)):
    if redis is None:
        return {"status": "error", "message": "Redis no está disponible en este entorno."}
    try:
        redis.set("grupo_8_test", "¡Conexión exitosa a Redis de forma correcta! ")
        value = redis.get("grupo_8_test")
        return {"redis_status": "OK", "valor_recuperado": value}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    