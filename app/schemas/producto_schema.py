from pydantic import BaseModel
from datetime import date

class ProductoResponse(BaseModel):
    id_producto: int
    asin: str
    titulo: str
    marca: str | None = None
    categoria_principal: str | None = None
    descripcion: str | None = None
    precio: float | None = None
    fecha_publicacion: date | None = None
    posicion: int | None = None
    imagenes: list[str] | None = None

    class Config:
        from_attributes = True
        