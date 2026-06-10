from pydantic import BaseModel

class AtributoBase(BaseModel):
    clave: str
    valor: str

class AtributoCreate(AtributoBase):
    id_producto: int

class AtributoResponse(AtributoBase):
    id_atributo: int
    id_producto: int

    class Config:
        from_attributes = True