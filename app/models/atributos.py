from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class Atributo(Base):
    __tablename__ = 'atributos'

    id_atributo: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_producto: Mapped[int] = mapped_column(ForeignKey("productos.id_producto", ondelete="CASCADE"), nullable=False)
    clave: Mapped[str] = mapped_column(String(50), nullable=False)
    valor: Mapped[str] = mapped_column(Text, nullable=False) 

    # Relación bidireccional moderna apuntando a la clase Producto
    producto: Mapped["Producto"] = relationship(back_populates="atributos")