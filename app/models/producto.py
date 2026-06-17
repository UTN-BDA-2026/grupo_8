from datetime import date
from decimal import Decimal
from typing import List
from sqlalchemy import String, Text, Numeric, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base
from app.models.ranking import Ranking
from sqlalchemy.dialects.postgresql import TSVECTOR

class Producto(Base):
    __tablename__ = "productos"

    id_producto: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    asin: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    titulo: Mapped[str] = mapped_column(Text, nullable=True) 
    marca: Mapped[str] = mapped_column(String(100), nullable=True)
    categoria_principal: Mapped[str] = mapped_column(String(100), nullable=True)
    descripcion: Mapped[str] = mapped_column(Text, nullable=True)
    precio: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=True) 
    fecha_publicacion: Mapped[date] = mapped_column(Date, nullable=True)
    search_vector: Mapped[any] = mapped_column(TSVECTOR, nullable=True)
 
    id_categoria: Mapped[int] = mapped_column(ForeignKey("categorias.id_categoria"), nullable=False, index=True)
    categoria: Mapped["Categoria"] = relationship(back_populates="productos")


    atributos: Mapped[List["Atributo"]] = relationship(back_populates="producto", cascade="all, delete-orphan")
    ranking: Mapped["Ranking"] = relationship(back_populates="producto", cascade="all, delete-orphan", uselist=False)
    relaciones: Mapped[List["Relacion"]] = relationship(back_populates="producto", cascade="all, delete-orphan")