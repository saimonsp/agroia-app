from sqlalchemy import Column, Integer, String, Float
from ..db import Base
from . import models, crud  # Ajuste para importação relativa

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    predictions = Column(String)  # Ou outro tipo que faça sentido
    heatmap_image = Column(String)  # Para armazenar a imagem do heatmap
