from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class Relacion(Base):
    __tablename__ = "relaciones"

    id_relacion: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_producto: Mapped[int] = mapped_column(ForeignKey("productos.id_producto", ondelete="CASCADE"), nullable=False)
    asin_relacionado: Mapped[str] = mapped_column(String(20), nullable=False)
    tipo_relacion: Mapped[str] = mapped_column(String(20), nullable=False)
    producto: Mapped["Producto"] = relationship(back_populates="relaciones")