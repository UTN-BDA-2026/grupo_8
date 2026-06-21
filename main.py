from fastapi import FastAPI, Depends
from app.db.session import get_db, engine
from sqlalchemy.orm import Session
from app.db.base_class import Base
from app.api.endpoints.categorias import router as categorias_router
from app.api.endpoints.atributo import router as atributos_router
from app.api.endpoints.producto import router as productos_router
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