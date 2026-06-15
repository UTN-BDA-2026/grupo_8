from pydantic import BaseModel

class RankingBase(BaseModel):
    id_categoria: int
    puntos: int 

class RankingCreate(RankingBase):
    pass    

class RankingResponse(RankingBase):
    id: int

    class Config:
        from_attributes = True  
        