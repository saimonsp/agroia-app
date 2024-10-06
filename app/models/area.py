from sqlalchemy import Column, Integer, Float
from app.db.database import Base

class Area(Base):
    __tablename__ = "areas"

    id = Column(Integer, primary_key=True, index=True)
    hectares = Column(Float, nullable=False)
    radius = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
