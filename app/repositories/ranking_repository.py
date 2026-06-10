from sqlalchemy.orm import Session
from sqlalchemy import select   
from typing import Optional
from app.models import Ranking

class RankingRepository:
    def get_by_id(self, db: Session, id_buscar: int) -> Optional[Ranking]:
        query = select(Ranking).where(Ranking.id == id_buscar)
        result = db.execute(query)
        return result.scalar()

ranking_repo = RankingRepository()  