from fastapi import FastAPI, Depends
from app.db.session import get_db, engine
from sqlalchemy.orm import Session
from app.db.base_class import Base

app = FastAPI(title="Buscador de Productos con FastAPI")

@app.get("/")
def home():
    return {"message": "API del buscador levantada correctamente"}

@app.get("/test-db")
def probar_conexion(db: Session = Depends(get_db)):
    return {"status": "Conectado a la base de datos exitosamente", "database": str(db)}