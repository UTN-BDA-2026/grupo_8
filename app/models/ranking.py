from sqlalchemy import Integer, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class Ranking(Base):
    __tablename__ = "ranking"

    id_ranking: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_producto: Mapped[int] = mapped_column(ForeignKey("productos.id_producto", ondelete="CASCADE"), nullable=False)
    id_categoria: Mapped[int] = mapped_column(ForeignKey("categorias.id_categoria", ondelete="CASCADE"), nullable=False)
    posicion: Mapped[int] = mapped_column(nullable=False)

    # Relaciones
    producto: Mapped["Producto"] = relationship(back_populates="ranking")
    categoria: Mapped["Categoria"] = relationship(back_populates="rankings")

    __table_args__ = (
        Index(
            "idx_ranking_categoria_posicion",
            "id_categoria",   # ahora indexa por id_categoria
            "posicion"       # y ordena por posición
        ),
    )


