from pydantic import BaseModel

class AreaCreate(BaseModel):
    hectares: float
    radius: float
    latitude: float
    longitude: float

class Area(AreaCreate):
    id: int

    class Config:
        orm_mode = True
