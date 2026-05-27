from pydantic import BaseModel

class CategoriaResponse(BaseModel):
    id_categoria: int
    id_producto: int
    nombre: str

    class Config:
        from_attributes = True