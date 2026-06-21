from datetime import date
from decimal import Decimal
from typing import List
from sqlalchemy import String, Text, Numeric, Date, ForeignKey, Index, func, text 
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base
from app.models.ranking import Ranking
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy import Index

class Producto(Base):
    __tablename__ = "productos"

    id_producto: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    asin: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    titulo: Mapped[str] = mapped_column(Text, nullable=True) 
    marca: Mapped[str] = mapped_column(String(300), nullable=True)
    descripcion: Mapped[str] = mapped_column(Text, nullable=True)
    precio: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=True) 
    fecha_publicacion: Mapped[date] = mapped_column(Date, nullable=True)
    search_vector: Mapped[any] = mapped_column(TSVECTOR, nullable=True)
    id_categoria: Mapped[int] = mapped_column(ForeignKey("categorias.id_categoria"), nullable=False, index=True)

    
    categoria: Mapped["Categoria"] = relationship(back_populates="productos")
    atributos: Mapped[List["Atributo"]] = relationship(back_populates="producto", cascade="all, delete-orphan")
    ranking: Mapped["Ranking"] = relationship(back_populates="producto", cascade="all, delete-orphan", uselist=False)
    relaciones: Mapped[List["Relacion"]] = relationship(back_populates="producto", cascade="all, delete-orphan")

    __table_args__ = (
        # Este índice guarda los títulos ya en minúsculas
        Index("ix_productos_titulo_lower", func.lower(text("titulo"))),
        # índice GIN para full-text search
        Index("ix_productos_search_vector", "search_vector", postgresql_using="gin"),
        # índice GIN para trigram similarity
        Index("ix_productos_titulo_trgm", "titulo", postgresql_using="gin", postgresql_ops={"titulo": "gin_trgm_ops"}),
    )