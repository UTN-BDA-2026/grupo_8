from pydantic import BaseModel

class CategoriaBase(BaseModel):
    nombre: str

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaResponse(CategoriaBase):
    id_categoria: int

    class Config:
        from_attributes = True