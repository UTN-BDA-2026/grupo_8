from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

from app.models.atributos import Atributo


class AtributoRepository:

    # Buscar atributos por id de producto
    def buscar_por_producto(self,db: Session, id_producto: int) -> List[Atributo]:

        consulta = (
            select(Atributo)
            .where(Atributo.id_producto == id_producto)
        )

        resultado = db.execute(consulta)

        return resultado.scalars().all()


    # Buscar atributos por clave
    def buscar_por_clave(
        self,
        db: Session,
        clave: str
    ) -> List[Atributo]:

        consulta = (
            select(Atributo)
            .where(Atributo.clave.ilike(f"%{clave}%"))
        )

        resultado = db.execute(consulta)

        return resultado.scalars().all()


    # Crear atributo
    def crear(
        self,
        db: Session,
        atributo: Atributo
    ) -> Atributo:

        db.add(atributo)
        db.commit()
        db.refresh(atributo)

        return atributo


atributo_repo = AtributoRepository()