from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base
from grupo_8.app.models.producto import Producto

class Imagen(Base):
    __tablename__ = "imagenes"

    id_imagen: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_producto: Mapped[int] = mapped_column( ForeignKey("productos.id_producto", ondelete="CASCADE"), nullable=False )
    url: Mapped[str] = mapped_column(Text, nullable=False)
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)

    producto: Mapped["Producto"] = relationship(back_populates="imagenes")
