from sqlalchemy import String, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class Ranking(Base):
    __tablename__ = "ranking"

    id_ranking: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_producto: Mapped[int] = mapped_column(ForeignKey("productos.id_producto", ondelete="CASCADE"), nullable=False)
    categoria: Mapped[str] = mapped_column(String(100), nullable=False)
    posicion: Mapped[int] = mapped_column(nullable=False)

    producto: Mapped["Producto"] = relationship(back_populates="rankings")


    __table_args__ = (
        Index(
            "idx_ranking_categoria_posicion",
            "categoria",      # 1° Busca por el texto de la categoría
            "posicion"        # 2° Ordena por la posición (agrega .desc() si el mayor número es el mejor)
        ),
    )
