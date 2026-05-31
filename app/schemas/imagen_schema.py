from pydantic import BaseModel

class ImagenResponse(BaseModel):
    id_imagen: int
    id_producto: int
    url: str
    tipo: str

    class Config:
        from_attributes = True   