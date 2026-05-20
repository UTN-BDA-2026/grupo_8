from fastapi import FastAPI
from app.db.database import engine

app = FastAPI()

@app.get("/")
def home():

    connection = engine.connect()
    connection.close()

    return {"message": "Conexión OK"}