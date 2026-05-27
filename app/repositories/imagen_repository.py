from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from app.models.imagen import Imagen

class ImagenRepository:
    def buscar_por_tipo(self, db: Session, tipo_buscar: str) -> List[Imagen]:
        consulta = select(Imagen).where(Imagen.tipo.ilike(f"%{tipo_buscar}%"))
        resultado = db.execute(consulta)
        return resultado.scalars().all()

imagen_repo = ImagenRepository()
