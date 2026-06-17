from sqlalchemy import String
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class Categoria(Base):
    __tablename__ = "categorias"
    id_categoria: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)    

    productos: Mapped[List["Producto"]] = relationship(back_populates="categoria")
    rankings: Mapped[List["Ranking"]] = relationship(back_populates="categoria", cascade="all, delete-orphan")
